"""Example Kafka consumer."""

import json
import os

from kafka import KafkaConsumer, KafkaProducer
from transaction_details import parse

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
TRANSACTIONS_DETAILS_TOPIC = os.environ.get('TRANSACTIONS_DETAILS_TOPIC')
DATASOURCE = os.environ.get('DATASOURCE')

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

    source_url = 'https://etherscan.io/tx/'
    for message in consumer:
        transaction: dict = message.value
        
        # get transaction details
        if('txhash' in transaction):
            (item, is_mined) = parse(source_url, transaction['txhash'])
            if(is_mined):                
                topic = TRANSACTIONS_DETAILS_TOPIC
                transaction: dict = item
                producer.send(topic, value=transaction)
                # print(topic, transaction)  # DEBUG
            else:
                pass
                # print('unmined')
