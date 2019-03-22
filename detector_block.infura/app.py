"""Example Kafka consumer."""

import json
import os
from time import sleep

from kafka import KafkaConsumer, KafkaProducer
from get_transactions_from_block import get_transactions_from_block

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
RAW_BLOCKS_TOPIC = os.environ.get('RAW_BLOCKS_TOPIC')
# TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_BLOCKTIME_TOPIC')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
TRANSACTIONS_BLOCK_TOPIC = os.environ.get('TRANSACTIONS_BLOCK_TOPIC')
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
        try: 
            if('blockhash' in message.value):
                value = message.value
                print(value)          
                blockhash = value['blockhash']                
                # Get transactoin hashes and blocktime of the block
                query = '{"jsonrpc":"2.0","method":"eth_getBlockByHash","params": ["'
                query += blockhash
                query += '",false],"id":1}'
                block_details = get_transactions_from_block(SOURCE_BLOCKDETAILS_URL, query)
                block_details = json.loads(block_details)
                if('result' in block_details):
                    result = block_details['result']
                    # result = json.loads(result)
                    # for key, value in block_details.items() :
                    #     print (key, value)
                    transactions = result['transactions']
                    endtime = result['timestamp']
                    blocknumber = result['number']
                    
                    # Send out topic about blocknumber and blocktime
                    transaction_block : dict = {'blocktime': endtime,'blocknumber':blocknumber}
                    producer.send(TRANSACTIONS_BLOCK_TOPIC, value=transaction_block)
                    print(TRANSACTIONS_BLOCK_TOPIC, transaction_block)  # DEBUG

                    for txhash in transactions:
                        transaction: dict = {'txhash': txhash, 'blocktime': endtime,'blocknumber':blocknumber }
                        topic = TRANSACTIONS_TOPIC
                        producer.send(topic, value=transaction)
                        print(topic, transaction)  # DEBUG

        except Exception as e:
            print(e)
        
        finally:
            pass
