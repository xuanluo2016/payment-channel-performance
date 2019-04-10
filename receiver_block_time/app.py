import os
import json

from kafka import KafkaConsumer, KafkaProducer

import config
import mysql.connector

TRANSACTIONS_BLOCK_TOPIC = os.environ.get('TRANSACTIONS_BLOCK_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
NUMBER_OF_CONFIRMATIONS = int(os.environ.get('NUMBER_OF_CONFIRMATIONS'))
BATCH_INTERVAL = int(os.environ.get('BATCH_INTERVAL'))

TABLE = config.Table
DATABASE = config.Database

if __name__ == '__main__':
    consumer = KafkaConsumer(
        TRANSACTIONS_BLOCK_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
    )

    # Connect to mysql db
    ctx = mysql.connector.connect(
        host = config.Host,
        user = config.User,
        passwd = config.Passwd,
        database = config.Database
        )

    for message in consumer:
        try:
           if('blocknumber' in message.value):
               value = message.value
            #    print(value)
               block_time = int(value['blocktime'],16)
               
               # Get the block number which is 12 blocks ahead
               block_number = int(value['blocknumber'], 16)
               prev_blocknumber = block_number - NUMBER_OF_CONFIRMATIONS + 1
               
            #    print('prev_blocknumber :', prev_blocknumber)
               # Get the blocktime of previous block ahead of number of confirmations
               cursor = ctx.cursor(buffered=True)
               query = "select * from " + TABLE + " where blocknumber = " + str(prev_blocknumber)
               cursor.execute(query)
               print('333')
               for row in cursor:
                   # Get the delta of time for blocks
                   prev_block_time = row[2]
                   block_time_delta = block_time - prev_block_time

                   query = "SET SQL_SAFE_UPDATES = 0"
                   cursor.execute(query)

                   #Update transactions which are 12 blocks earlier
                   query = "update " +  config.Table + " SET waitingtime =  " + str(block_time_delta) + " where blocknumber = " + str(prev_blocknumber)
                   cursor.execute(query)
                   ctx.commit()
                   print("updated rows of waiting time = {}".format(cursor.rowcount))
                   break
               cursor.close()                
        except Exception as e:
            print(e)
                
        finally:
            pass
    




