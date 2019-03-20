"""Produce fake transactions into a Kafka topic."""

import os
import time
from time import sleep
from datetime import datetime
import json
import requests
from kafka import KafkaProducer

RAW_TRANSACTIONS_TOPIC = os.environ.get('RAW_TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND 
REQUEST_INTERVAL =  float(os.environ.get('REQUEST_INTERVAL')) 
SOURCE_URL = os.environ.get('SOURCE_URL')

def publish_message(message):
    """public the response of the website to kafka."""
    print('publish message')
    timestamp = time.time()
    timestamp_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
  
    transaction: dict = {"data": message, "time": timestamp_date, "seconds": timestamp }
    producer.send(RAW_TRANSACTIONS_TOPIC, value=transaction)
    # print(RAW_TRANSACTIONS_TOPIC,transaction ) # DEBUG


if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )
            
    while True:
        try:
            response = requests.get(SOURCE_URL)
            if(response != None):
                publish_message(response.content.decode())

            sleep(REQUEST_INTERVAL)
            
        except Exception as e:
            print("#######################error in generator############################")
            print(e)
            
        finally:
            pass
