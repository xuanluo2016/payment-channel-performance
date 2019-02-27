"""Example Kafka consumer."""

import json
import os
from time import sleep

from kafka import KafkaConsumer, KafkaProducer
from get_transactions_from_block import get_transactions_from_block

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
RAW_BLOCKS_TOPIC = os.environ.get('RAW_BLOCKS_TOPIC')
TRANSACTIONS_BLOCKTIME_TOPIC = os.environ.get('TRANSACTIONS_BLOCKTIME_TOPIC')
SOURCE_BLOCKDETAILS_URL = os.environ.get('SOURCE_BLOCKDETAILS_URL')

if __name__ == '__main__':
    consumer = KafkaConsumer(
        RAW_BLOCKS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    for message in consumer:
        if('data' in message.value):
            value = message.value
            time = value['time']
            seconds = value['seconds']
            data = json.loads(value['data'])
            print("========================================")
            print(data)
            print("========================================")

            for row in data:
                # get transactoin hash of the block
                query = '{"jsonrpc":"2.0","method":"eth_getBlockByHash","params": ["'
                query += row
                query += '",false],"id":1}'
                block_details = get_transactions_from_block(SOURCE_BLOCKDETAILS_URL, query)

                if('timstamp' in block_details):
                    endtime = block_details['timestamp']
                    transactions =  block_details['transactions']
                    for txhash in transactions:
                        transaction: dict = {'txhash': row, 'endtime': timestamp, 'seconds': seconds}
                        topic = TRANSACTIONS_BLOCKTIME_TOPIC
                        producer.send(topic, value=transaction)
                        print(topic, transaction)  # DEBUG
                        sleep(1)
