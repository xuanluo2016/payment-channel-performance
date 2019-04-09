import os
import json

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import config
from lib.db import DB
import mysql.connector


from get_transaction_details import parse
from get_transaction_summary import get_summary

MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_BLOCK_TOPIC')
KAFKA_ZOOKEEPER_CONNECT = os.environ.get('KAFKA_ZOOKEEPER_CONNECT')
NUMBER_OF_CONFIRMATIONS = int(os.environ.get('NUMBER_OF_CONFIRMATIONS'))
BATCH_INTERVAL = int(os.environ.get('BATCH_INTERVAL'))

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.0 pyspark-shell --master spark://master:7077 '

TABLE = config.Table
DATABASE = config.Database

def pprint2(lines,ctx):
    """
    Print the first num elements oNUMBER_OF_CONFIRMATIONSf each RDD generated in this DStream.

    @param num: the number of elements from the first will be printed.
    """
    def takeAndPrint(rdd):
        collect = rdd.collect() 
        for record in collect:            
            process_record(ctx,record)

    lines.foreachRDD(takeAndPrint)

def process_record(ctx,record):
    """
    Check if the txhash exists or not in the end_time table
    if yes, send streaming data to query tx details and remove related record in the end_time db
    else, save data in the start_time db
    """
    print(record)
    record = json.loads(record)
    if('blocknumber' in record):
        try: 
            print('111')
            block_time = int(record['blocktime'],16)

            # Get the block number which is 12 blocks ahead
            block_number = record['blocknumber']
            block_number = int(block_number, 16)
            prev_blocknumber = block_number - NUMBER_OF_CONFIRMATIONS + 1

            print('222')
            # Get the blocktime of previous block ahead of number of confirmations
            cursor = ctx.cursor()
            query = "select * from " + TABLE + " where blocknumber = " + str(prev_blocknumber)
            cursor.execute(query)
            print('333')
            for row in cursor:
                # Get the delta of time for blocks
                prev_block_time = row[2]
                block_time_delta = block_time - prev_block_time
            
                #Update transactions which are 12 blocks earlier
                query = "update " + TABLE + " SET waiting_time = " + str(block_time_delta) +  "where blocknumber = " + str(prev_blocknumber)
                newcursor = ctx.cursor()
                newcursor.execute(query)
                ctx.commit()
                print("updated rows of waiting time = {}".format(newcursor.rowcount))
                newcursor.close()
                break 
            cursor.close()

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
conf = SparkConf().setAppName("PythonSparkStreamingKafkaEndTimeApp1")


# Create a SparkContext using the configuration
sc = SparkContext(conf=conf)

# Set log level
sc.setLogLevel("ERROR")

# Create the streaming contect objects
ssc = StreamingContext(sc,BATCH_INTERVAL)

# Create the kafka connection object
# kafkaStream = KafkaUtils.createStream(ssc, ["starttime"], {"metadata.broker.list": "localhost:9092" ,TRANSACTIONS_DETAILS_TOPIC:1})
kafkaStream = KafkaUtils.createStream(ssc, KAFKA_ZOOKEEPER_CONNECT, "spark-streaming-blocktime", {TRANSACTIONS_TOPIC:1})

lines = kafkaStream.map(lambda x: x[1])

# # connect to mongodb
# db_connection =  DB()
# db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]

# col_block_time = db["block_time"]
# col_block_time.create_index([('blocknumber', pymongo.ASCENDING)], unique = True)

# col_summary = db["summary"]

# Connect to mysql db
ctx = mysql.connector.connect(
    host = "ethfullnodedb.c0cwkssklnbh.us-west-2.rds.amazonaws.com",
    user = "admin",
    passwd = "l3ft0fth3d0t",
    database = config.Database
    )

# insert data to mongo db
pprint2(lines,ctx)

# start ssc
ssc.start()
ssc.awaitTermination()

