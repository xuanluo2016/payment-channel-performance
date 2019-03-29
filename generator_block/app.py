"""Produce fake transactions into a Kafka topic."""

import os
import json
import websocket

from datetime import datetime
from time import sleep
from kafka import KafkaProducer
from get_current_block import get_current_block

RAW_BLOCKS_TOPIC = os.environ.get('RAW_BLOCKS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND 
REQUEST_INTERVAL =  float(os.environ.get('REQUEST_INTERVAL')) 
SOURCE_URL = os.environ.get('SOURCE_URL')
NUMBER_OF_CONFIRMATIONS = int(os.environ.get('NUMBER_OF_CONFIRMATIONS'))

if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    
    latest_block_number = ''
    current_block_number = ''

    while True:
        try:
            query = '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
            message = get_current_block(SOURCE_URL, query)
            print(message)
            print(type(message))
            message = json.loads(message)
            if('result' in message):
                latest_block_number = message['result']
                if(latest_block_number != current_block_number) and (latest_block_number != ''):
                    current_block_number = latest_block_number
                    # get the block number which are 12 blocks older
                    block_number = latest_block_number
                    block_number = int(block_number, 16)
                    prev_blocknumber = block_number - NUMBER_OF_CONFIRMATIONS + 1
                    prev_blocknumber = hex(prev_blocknumber)

                    # Send a new item to block topic
                    transaction:dict = {"blocknumber": prev_blocknumber}
                    topic = RAW_BLOCKS_TOPIC
                    producer.send(topic, value=transaction)

            # Wait for a while before sending out next request
            sleep(REQUEST_INTERVAL)

        except Exception as e:
            print("#######################error in generator block############################")
            print(e)
            
        finally:
            pass