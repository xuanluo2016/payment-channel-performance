"""Example Kafka consumer."""

import json
import os
from time import sleep

import pymongo
from pymongo.errors import BulkWriteError
from lib.db import DB

from kafka import KafkaConsumer, KafkaProducer
from get_transactions_from_block import get_transactions_from_block

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
RAW_BLOCKS_TOPIC = os.environ.get('RAW_BLOCKS_TOPIC')
# TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_BLOCKTIME_TOPIC')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
TRANSACTIONS_BLOCK_TOPIC = os.environ.get('TRANSACTIONS_BLOCK_TOPIC')
SOURCE_BLOCKDETAILS_URL = os.environ.get('SOURCE_BLOCKDETAILS_URL')
MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')

if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )

    # connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]

    col_block_time = db["block_time"]

    doc = col_block_time.find()
    count = 0
    for row in doc:
        transaction_block : dict = {'blocktime': hex(row['blocktime']),'blocknumber':hex(row['blocknumber'])}
        producer.send(TRANSACTIONS_BLOCK_TOPIC, value=transaction_block)
        print(TRANSACTIONS_BLOCK_TOPIC, transaction_block)  # DEBUG
        count = count + 1
        print(count)
    print('number of updated items: ', count)