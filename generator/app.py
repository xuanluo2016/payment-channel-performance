"""Produce fake transactions into a Kafka topic."""

import os
from time import sleep
import json

from kafka import KafkaProducer
from transactions import create_random_transaction

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

from datetime import datetime


TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND
print('sleep_time is: ' + str(SLEEP_TIME))
request = []


# return substr between two substrings in a string
# return '' if the input is invalid or could not find the substr; else return substr
def get_substr(str, substr1, substr2) -> str:
  if(str == None):
      return ''

  left = str.find(substr1)
  right = str.find(substr2)

  if(left == -1) or (right == -1):
    return ''
  else:
    return str[left+len(substr1):right]

def on_message(ws, message):
    print('----------------------------message------------------')
    print(message)
    if (len(request) != 0):
        #print('asking for filter change')
        query = {"data": message, "time": datetime.now(), "seconds":''}
        ws.send(request[0])
        sleep(SLEEP_TIME)
    else:
        # print('ask for the filter id')
        substr1 = '"result":'
        substr2 = '}'
        id = get_substr(message, substr1, substr2)

        # send request to get pending transactions
        str1 = '{"jsonrpc":"2.0","method":"eth_getFilterChanges","params":['
        str2 = '],"id":1}'
        request.append(str1 + id + str2)
        ws.send(request[0])
    

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            request = []
            print("------------------------------open---------------------------------")
            ws.send('{"jsonrpc":"2.0","method":"eth_newPendingTransactionFilter","params":[],"id":1}')
        # time.sleep(1)
        # ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )

    while True:
        try: 
            websocket.enableTrace(False)
            ws = websocket.WebSocketApp("wss://mainnet.infura.io/ws",
                                        on_message = on_message,
                                        on_error = on_error,
                                        on_close = on_close)
            ws.on_open = on_open
            ws.run_forever()

            transaction: dict = create_random_transaction()
            producer.send(TRANSACTIONS_TOPIC, value=transaction)
            # print(transaction)  # DEBUG
            sleep(SLEEP_TIME)
        except:
            pass
