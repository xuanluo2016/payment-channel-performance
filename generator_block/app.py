"""Produce fake transactions into a Kafka topic."""

import os
import json
import websocket

from datetime import datetime
from time import sleep
from kafka import KafkaProducer

RAW_BLOCKS_TOPIC = os.environ.get('RAW_BLOCKS_TOPIC')
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
    """Extract block hashes and related timestamp from raw websocket message."""
    try: 
        dict_message = json.loads(message)
        #{"jsonrpc":"2.0","id":1,"result":["0x372521f455740308b4f9f131976480cb7217c9a869c1a69aac748f1083be97c2","0x08cde2da1228ee8d95e13ad1663f079d0c6c11072b0ea687d2c11aac5b8da6a2"]}

        if('result' in dict_message):
            blocks = dict_message['result']
            # print(type(blocks))
            for blockhash in blocks:    
                transaction:dict = {"blockhash": blockhash, }
                topic = RAW_BLOCKS_TOPIC
                producer.send(topic, value=transaction)
                print(topic, transaction)  # DEBUG
    except Exception as e:
        pass

    # try: 
    #     print("++++++++++++++++++++++++++++++++++++++")
    #     print(message)
    #     print("++++++++++++++++++++++++++++++++++++++")
    #     # dict_message = json.loads(message)

    #     dict_message = message        
    #     if('result' in dict_message):
    #         result = dict_message['result']
    #         if(len(result) > 0):
    #             blocks = json.dumps(result)
    #             print("++++++++++++++++++++++++++++++++++++++")
    #             print(blocks)
    #             print("++++++++++++++++++++++++++++++++++++++")
    #             for blockhash in blocks:
    #                 transaction: dict = {'blockhash': blockhash}
    #                 topic = RAW_BLOCKS_TOPIC
    #                 producer.send(topic, value=transaction)
    #                 print(topic, transaction)  # DEBUG

    # except Exception as e:
    #     print("#######################error in publish_message of generator_block ############################")
    #     print(e.message)
    # finally: 
    #     pass

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
            ws.send('{"jsonrpc":"2.0","method":"eth_newBlockFilter","params":[],"id":1}')
    # thread.start_new_thread(run, ())
    request = []
    ws.send('{"jsonrpc":"2.0","method":"eth_newBlockFilter","params":[],"id":1}')

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
    
    DEBUG = True

    while True:
        try:
            print("start websocket")
            websocket.enableTrace(False)

            ws = websocket.WebSocketApp(SOURCE_URL, on_message = on_message, on_error = on_error, on_close = on_close)
            ws.on_open = on_open
            ws.run_forever()
            sleep(SLEEP_TIME)
            
        except Exception as e:
            print("#######################error in generator############################")
            print(e)
            
        finally:
            pass

