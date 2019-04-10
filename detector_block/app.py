"""Example Kafka consumer."""

import json
import os
from time import sleep

from kafka import KafkaConsumer, KafkaProducer
from get_transactions_from_block import get_transactions_from_block
import config
import mysql.connector


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
RAW_BLOCKS_TOPIC = os.environ.get('RAW_BLOCKS_TOPIC')
# TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_BLOCKTIME_TOPIC')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
TRANSACTIONS_BLOCK_TOPIC = os.environ.get('TRANSACTIONS_BLOCK_TOPIC')
SOURCE_BLOCKDETAILS_URL = os.environ.get('SOURCE_BLOCKDETAILS_URL')
NUMBER_OF_CONFIRMATIONS = int(os.environ.get('NUMBER_OF_CONFIRMATIONS'))

TABLE = config.Table
DATABASE = config.Database

def initialize_db_and_table():  

	ctx =  mysql.connector.connect(
        host = config.Host,
        user = config.User,
        passwd = config.Passwd,
        database = config.Database
        )
	cursor = ctx.cursor()
	query = "CREATE TABLE IF NOT EXISTS " + TABLE + " (txhash VARCHAR(255) PRIMARY KEY, blocknumber int NOT NULL, blocktime DOUBLE(50,7) NOT NULL, waitingtime DOUBLE(50,7) )"
	cursor.execute(query)
	ctx.commit()
	print("affected rows = {}".format(cursor.rowcount))
	cursor.close()
	ctx.close()
	return

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

    # Create Table if not exist
    initialize_db_and_table()
    ctx =  mysql.connector.connect(
        host = config.Host,
        user = config.User,
        passwd = config.Passwd,
        database = config.Database
        )
    
    for message in consumer:
        try: 
            if('blocknumber' in message.value):
                value = message.value
                blocknumber = value['blocknumber']                
                # Get traTABLEnsactoin hashes and blocktime of the block
                query = '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params": ["'
                query += blocknumber
                query += '",false],"id":1}'
                block_details = get_transactions_from_block(SOURCE_BLOCKDETAILS_URL, query)
                block_details = json.loads(block_details)
                if('result' in block_details):
                    result = block_details['result']

                    transactions = result['transactions']
                    endtime = result['timestamp']
                    blocknumber = result['number']
                    gasused = result['gasUsed']
                    
                    # Send out topic about blocknumber and blocktime
                    transaction_block : dict = {'blocktime': endtime,'blocknumber':blocknumber, 'gasused':gasused}
                    producer.send(TRANSACTIONS_BLOCK_TOPIC, value=transaction_block)
                    print(TRANSACTIONS_BLOCK_TOPIC, transaction_block)  # DEBUG
                    
                   
                    # Insert tranasctions into end table
                    requests = []
                    for tx in transactions:
                        temp = []
                        temp.append(tx)
                        temp.append(int(blocknumber,16))
                        temp.append(int(endtime,16))
                        temp.append(0)
                        requests.append(temp)
                    if(len(requests) > 0):
                        cursor = ctx.cursor()                   
                        sql_insert_query =  "INSERT IGNORE INTO " + TABLE  + " (txhash,blocknumber,blocktime,waitingtime) VALUES  (%s, %s, %s, %s)"
                        cursor.executemany(sql_insert_query, requests)  
                        ctx.commit()
                        print("affected rows = {}".format(cursor.rowcount))
                        cursor.close()
                        requests.clear()
                    
                    # # Update Records which are 12 confirmations ahead
                    # block_number = int(blocknumber, 16)
                    # prev_blocknumber = block_number - NUMBER_OF_CONFIRMATIONS + 1
                    # query = "select * from " + TABLE + " where blocknumber = " + str(prev_blocknumber)
                    # cursor.execute(query)
                    # for row in cursor:
                    #     # Get the delta of time for blocks
                    #     prev_block_time = row[2]
                    #     block_time_delta = block_time - prev_block_time
                    
                    #     #Update transactions which are 12 blocks earlier
                    #     query = "update " + TABLE + " SET waitingtime = " + str(block_time_delta) +  "where blocknumber = " + str(prev_blocknumber)
                    #     cursor.execute(query)
                    #     ctx.commit()
                    #     print("updated rows of waiting time = {}".format(cursor.rowcount))                        
                    #     break

                    

        except Exception as e:
            print(e)
        
        finally:
            pass
