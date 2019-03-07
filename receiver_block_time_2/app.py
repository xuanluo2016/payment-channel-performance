import os
import json

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import pymongo
from pymongo.errors import BulkWriteError
from lib.db import DB

from get_transaction_details import parse
from get_transaction_summary import get_summary

MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_BLOCK_TOPIC')
KAFKA_ZOOKEEPER_CONNECT = os.environ.get('KAFKA_ZOOKEEPER_CONNECT')
NUMBER_OF_CONFIRMATIONS = int(os.environ.get('NUMBER_OF_CONFIRMATIONS'))
BATCH_INTERVAL = int(os.environ.get('BATCH_INTERVAL'))

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.0 pyspark-shell --master spark://master:7077 '


def pprint2(lines,col_block_time,col_summary):
    """
    Print the first num elements oNUMBER_OF_CONFIRMATIONSf each RDD generated in this DStream.

    @param num: the number of elements from the first will be printed.
    """
    # def takeAndPrint(rdd):
    #     taken = rdd.take(num + 1) 
    #     for record in taken[:num]:            
    #         process_record(col_start_time,col_end_time, col_summary, record)
    #         if len(taken) > num:
    #             print("...")
    #             print("")

    def takeAndPrint(rdd):
        collect = rdd.collect() 
        for record in collect:            
            process_record(col_block_time,col_summary,record)

    lines.foreachRDD(takeAndPrint)

    # lines.foreachRDD(takeAndPrint)

def process_record(col_block_time,col_summary,record):
    """
    Check if the txhash exists or not in the end_time table
    if yes, send streaming data to query tx details and remove related record in the end_time db
    else, save data in the start_time db
    """
    record = json.loads(record)
    print(record)
    if('blocknumber' in record):
        try: 
            block_time = int(record['blocktime'],16)

            # Get the block number which is 12 blocks ahead
            block_number = record['blocknumber']
            block_number = int(block_number, 16)
            prev_blocknumber = block_number - NUMBER_OF_CONFIRMATIONS
            prev_blocknumber = hex(prev_blocknumber)


            # Get the blocktime of previous block ahead of number of confirmations
            doc = col_block_time.find_one({'blocknumber': prev_blocknumber})
            if(doc != None):
                # Get the delta of time for blocks

                prev_block_time = doc['blocktime']
                prev_block_time = int(prev_block_time,16)
                block_time_delta = block_time - prev_block_time
            
                #Update transactions which are 12 blocks earlier
                post = {"waiting_time": block_time_delta}
                col_summary.update_many({'blocknumber': prev_blocknumber},  {'$set': post}) 
                print('update summary table')

            # # Find transactions which are 12 blocks ahead
            # doc = col_summary.find({"blocknumber": prev_blocknumber} )

            # for row in doc:
            #     prev_block_time = row['blocktime']
            #     block_time_delta = block_time - prev_block_time
            #     waiting_time = block_time_delta + row['waiting_time']
            #     # query = '{_id: ' + row['_id'] + '}, {$set: {"waiting_time": ' + str(waiting_time) + '}}'
            #     # print(query)
            #     # result = col_summary.update(query)
            #     post = {"waiting_time": waiting_time}
            #     # col_summary.update_one({"_id":'ObjectId("5c7b78046fd11d5872ff4be3")'},  {"$set": post}) 
            #     result = col_summary.update_one({"txhash":row['txhash']},  {"$set": post})  
            #     print(result)
            #     print(row['txhash']) 

            # insert block_time and block_number to table block_time
            print('insert into block collection: ')
            col_block_time.insert(record)

        except Exception as e:
            print(e)
            
        finally:
            pass
   
    return

# mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = mongo_client["transactions"]
# col = db["start_time"]
# col.find({}, no_cursor_timeout=True).limit(30)


# Create a basic configuration
# conf = SparkConf().setAppName("PythonSparkStreamingKafkaEndTimeApp").setMaster("spark://master:7077")
conf = SparkConf().setAppName("PythonSparkStreamingKafkaEndTimeApp2")


# Create a SparkContext using the configuration
sc = SparkContext(conf=conf)

# Set log level
sc.setLogLevel("ERROR")

# Create the streaming contect objects
ssc = StreamingContext(sc,BATCH_INTERVAL)

# Create the kafka connection object
# kafkaStream = KafkaUtils.createStream(ssc, ["starttime"], {"metadata.broker.list": "localhost:9092" ,TRANSACTIONS_DETAILS_TOPIC:1})
kafkaStream = KafkaUtils.createStream(ssc, KAFKA_ZOOKEEPER_CONNECT, "spark-streaming-blocktime2", {TRANSACTIONS_TOPIC:1})

lines = kafkaStream.map(lambda x: x[1])

# connect to mongodb
db_connection =  DB()
db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]

col_block_time = db["block_time"]
col_block_time.create_index([('blocknumber', pymongo.ASCENDING)], unique = True)

col_summary = db["summary"]

# insert data to mongo db
pprint2(lines,col_block_time,col_summary)

# start ssc
ssc.start()
ssc.awaitTermination()

