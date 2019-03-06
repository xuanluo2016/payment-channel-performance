print('test')
import pymongo
from pymongo.errors import BulkWriteError
from lib.db import DB
from time import sleep
import os

from get_transaction_details import parse
from get_transaction_summary import get_summary

MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')
BATCH_INTERVAL = int(os.environ.get('BATCH_INTERVAL'))
NUMBER_OF_CONFIRMATIONS = int(os.environ.get('NUMBER_OF_CONFIRMATIONS'))

# connect to mongodb
db_connection =  DB()
db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]

col_start_time = db["start_time"]
col_end_time = db["end_time"]
col_block_time = db["block_time"]
col_summary = db["summary"]

print('sleep')
dict_blocks = {} # int, int

count = 0 

while(True):

    try: 
        count = count + 1
        # doc = col_start_time.find_one({'handled': {'$ne': True}})
        # col_start_time.aggregate([{'handled': {'$ne': True}}])
        doc_start_time = col_start_time.aggregate([
            { "$match": {'handled': {'$ne': True} } },
            { "$sample": { "size": 100 } }
        ])

        for doc in doc_start_time:
            start_time = doc['seconds']

            tx_hash = doc['txhash']
            print('txhash: ', tx_hash)

            # Get end time
            # doc_end_time = col_end_time.find_one({'txhash': tx_hash, 'handled': {'$ne': True}})
            doc_end_time = col_end_time.find_one({"$and": [{'txhash': tx_hash}, {'handled': {'$ne': True}}]})

            if(doc_end_time != None):
                end_time = int(doc_end_time['blocktime'],16)
                print('end time: ', end_time)

                # Get blocktime when receiving certain amount of confirmations
                block_number = int(doc_end_time['blocknumber'], 16)

                # Store blocktime and block numbr in dict
                dict_blocks[block_number] = end_time

                # See if there are enough confirmations for the transaction
                confirm_blocknumber = block_number + NUMBER_OF_CONFIRMATIONS
                block_time_delta = 0
                if(confirm_blocknumber in dict_blocks):
                    block_time_delta = dict_blocks[confirm_blocknumber] - end_time
                else:
                    doc_block_time = col_block_time.find_one({'blocknumber': confirm_blocknumber})
                    if(doc_block_time != None):
                        confirm_block_time = int(doc_block_time['blocktime'],16)
                        block_time_delta = confirm_block_time - end_time
                
                print('block_time_delta: ', block_time_delta)

                # Insert data into summary and mark related data from start_time and end_time as hanled
                if(block_time_delta != 0):
                    (item, is_mined) = parse(URL, record['txhash'])
                    if(is_mined):
                        row = get_summary(item, tx_hash, start_time, end_time, hex(block_number))
                        row['waiting_time'] = block_time_delta

                        # Insert data into summary collection
                        result = col_summary.insert(row)
                        print('summary: ', summary)

                        if(result.count() != None):
                            # Update related items
                            post = {"handled": True}
                            col_start_time.update_one({'txhash': tx_hash},  {'$set': post})
                            col_end_time.update_one({'txhash': tx_hash},  {'$set': post})
                            print("txhash", tx_hash)
    except Exception as e:
        print(e)

    finally:
        pass
    
sleep(BATCH_INTERVAL)
print(count)