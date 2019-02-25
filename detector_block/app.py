"""Example Kafka consumer."""

import json
import os
from time import sleep


from kafka import KafkaConsumer, KafkaProducer

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
RAW_BLOCKS_TOPIC = os.environ.get('RAW_BLOCKS_TOPIC')
TRANSACTIONS_BLOCKTIME_TOPIC = os.environ.get('TRANSACTIONS_BLOCKTIME_TOPIC')

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
            for row in data: 
                transaction: dict = {'txhash': row, 'time': time, 'seconds': seconds}
                topic = TRANSACTIONS_BLOCKTIME_TOPIC
                producer.send(topic, value=transaction)
                print(topic, transaction)  # DEBUG
                sleep(1)
