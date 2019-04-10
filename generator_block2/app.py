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
REQUEST_INTERVAL =  float(os.environ.get('REQUEST_INTERVAL')) 
NUMBER_OF_CONFIRMATIONS = int(os.environ.get('NUMBER_OF_CONFIRMATIONS'))
START_BLOCK = int(os.environ.get('START_BLOCK'))
END_BLOCK = int(os.environ.get('END_BLOCK'))


if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    
    current_block_number = START_BLOCK

    while (current_block_number < END_BLOCK):
        try:
            
            prev_blocknumber = current_block_number - NUMBER_OF_CONFIRMATIONS + 1
            prev_blocknumber = hex(prev_blocknumber)

            # Send a new item to block topic
            transaction:dict = {"blocknumber": prev_blocknumber}
            topic = RAW_BLOCKS_TOPIC
            producer.send(topic, value=transaction)
            print(topic, transaction)

            # Wait for a while before sending out next request
            sleep(REQUEST_INTERVAL)

            current_block_number = current_block_number + 1

        except Exception as e:
            print("#######################error in generator block############################")
            print(e)
            
        finally:
            pass

