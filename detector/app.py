"""Example Kafka consumer."""

import json
import os

from kafka import KafkaConsumer, KafkaProducer

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
RAW_TRANSACTIONS_TOPIC = os.environ.get('RAW_TRANSACTIONS_TOPIC')
LEGIT_TOPIC = os.environ.get('LEGIT_TOPIC')
FRAUD_TOPIC = os.environ.get('FRAUD_TOPIC')


def is_suspicious(transaction: dict) -> bool:
    """Determine whether a transaction is suspicious."""
    return len(transaction) >= 50   

if __name__ == '__main__':
    consumer = KafkaConsumer(
        RAW_TRANSACTIONS_TOPIC,
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
                topic = FRAUD_TOPIC if is_suspicious(transaction) else LEGIT_TOPIC
                producer.send(topic, value=transaction)
                print(topic, transaction)  # DEBUG
