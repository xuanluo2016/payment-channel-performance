"""Example Kafka consumer."""

import json
import os
from time import sleep


from kafka import KafkaConsumer, KafkaProducer

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
RAW_TRANSACTIONS_TOPIC = os.environ.get('RAW_TRANSACTIONS_TOPIC')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')

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
            data = value['data']
            # when there is only one transaction detected
            if(len(data) == 66):
                transaction: dict = {'txhash': data, 'starttime': time, 'seconds': seconds}
                topic = TRANSACTIONS_TOPIC
                producer.send(topic, value=transaction)
                print(topic, transaction)  # DEBUG
            
            # when there are more than one transaction detected     
            else:
                for row in data: 
                    transaction: dict = {'txhash': row, 'starttime': time, 'seconds': seconds}
                    topic = TRANSACTIONS_TOPIC
                    producer.send(topic, value=transaction)
                    print(topic, transaction)  # DEBUG
