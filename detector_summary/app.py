"""Example Kafka consumer."""

import json
import os
from time import sleep

import pymongo
from pymongo.errors import BulkWriteError
from lib.db import DB

from kafka import KafkaConsumer, KafkaProducer
from process_record import process_record

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
TRANSACTIONS_SUMMARY_TOPIC = os.environ.get('TRANSACTIONS_SUMMARY_TOPIC')
MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')

if __name__ == '__main__':
    consumer = KafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )

    # Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]

    col_start_time = db["start_time"]
    col_start_time.create_index([('txhash', pymongo.ASCENDING)], unique = True)

    col_end_time = db["end_time"]
    col_end_time.create_index([('txhash', pymongo.ASCENDING)], unique = True)

    col_summary = db["summary"]
    col_summary.create_index([('txhash', pymongo.ASCENDING)], unique = True)

    topic = TRANSACTIONS_SUMMARY_TOPIC

    for message in consumer:
        """
        Example: message: {'txhash': row, 'starttime': time, 'seconds': seconds}
        Example: message: {'txhash': txhash, 'blocktime': endtime, 'blocknumber':blocknumber}

        """
        if('txhash' in message.value):
            print('detector_summary')
            tx_hash = message.value['txhash']
            result = process_record(col_start_time, col_end_time, col_summary, message.value)
            print('result', result)
            # If the iteam has been inserted into summary table, send out a message for transaction details
            if(0 == result):
                print('sending summary topic')
                transaction: dict = {'txhash': tx_hash}
                producer.send(topic, value=transaction)
                print(topic, transaction)  # DEBUG