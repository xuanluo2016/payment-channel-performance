"""Produce fake transactions into a Kafka topic."""

import os
import time
from time import sleep
from datetime import datetime
import json

from kafka import KafkaProducer
import websocket


RAW_TRANSACTIONS_TOPIC = os.environ.get('RAW_TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND 
REQUEST_INTERVAL =  float(os.environ.get('REQUEST_INTERVAL')) 
SOURCE_URL = os.environ.get('SOURCE_URL')

request = []
producer = None

# Return substr between two substrings in a string
# Return '' if the input is invalid or could not find the substr; else return substr
def get_substr(str, substr1, substr2) -> str:
  if(str == None):
      return ''

  left = str.find(substr1)
  right = str.find(substr2)

  if(left == -1) or (right == -1):
    return ''
  else:
    return str[left+len(substr1):right]

def publish_message(message):
    """Extract transaction hashes and related timestamp from raw websocket message."""
    print('publish message')
    timestamp = time.time()
    timestamp_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    # print(timestamp)
    try: 
        dict_message = json.loads(message)
        if('result' in dict_message):
            result = dict_message['result']
            # if any transactions detected
            if(len(result) > 0):
                results = {"data": result, "time": timestamp_date, "seconds": timestamp }
                transaction: dict = results
                producer.send(RAW_TRANSACTIONS_TOPIC, value=transaction)
                print(RAW_TRANSACTIONS_TOPIC,transaction ) # DEBUG
    except Exception as e:
        print(e)    
    finally:
        pass

def is_required_data(message) -> bool:
    if('result' in message):
        return True
    else:
        return False

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(REQUEST_INTERVAL)
            request = []
            ws.send('{"jsonrpc":"2.0","method":"eth_newPendingTransactionFilter","params":[],"id":1}')
    # thread.start_new_thread(run, ())
    request = []
    ws.send('{"jsonrpc":"2.0","method":"eth_newPendingTransactionFilter","params":[],"id":1}')

def on_message(ws, message):
    if (len(request) != 0):
        # Send the received message to kafka
        publish_message(message)

        # Asking for filter change
        ws.send(request[0])

        # Sleep for some time before sending next websocket request
        sleep(REQUEST_INTERVAL)
    else:
        # Ask for the filter id
        substr1 = '"result":'
        substr2 = '}'
        id = get_substr(message, substr1, substr2)

        # Send request to get pending transactions
        str1 = '{"jsonrpc":"2.0","method":"eth_getFilterChanges","params":['
        str2 = '],"id":1}'
        request.append(str1 + id + str2)
        ws.send(request[0])
    

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")


if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )
            
    # DEBUG = True

    while True:
        try:
            print("start websocket")
            request.clear()
            websocket.enableTrace(False)

            ws = websocket.WebSocketApp(SOURCE_URL, on_message = on_message, on_error = on_error, on_close = on_close)
            ws.on_open = on_open
            ws.run_forever()
            sleep(15)
            
        except Exception as e:
            print("#######################error in generator############################")
            print(e)
            
        finally:
            pass
