import os
import json

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import pymongo
from pymongo.errors import BulkWriteError
from lib.db import DB

from get_transaction_details import parse

MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_BLOCKTIME_TOPIC')
KAFKA_ZOOKEEPER_CONNECT = os.environ.get('KAFKA_ZOOKEEPER_CONNECT')

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.0 pyspark-shell --master spark://master:7077 '


def pprint2(lines, col_start_time,col_end_time,col_summary, num=10):
    """
    Print the first num elements of each RDD generated in this DStream.

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
            process_record(col_start_time,col_end_time, col_summary, record)

    lines.foreachRDD(takeAndPrint)

    # lines.foreachRDD(takeAndPrint)

def process_record(col_start_time,col_end_time,col_summary,record):
    """
    Check if the txhash exists or not in the end_time table
    if yes, send streaming data to query tx details and remove related record in the end_time db
    else, save data in the start_time db
    """
    record = json.loads(record)

    if('txhash' in record): 
        doc = col_start_time.find({"txhash": record['txhash']} )
        try: 
            if(doc.count() >0):
                print("find record in start_time")
                # Send tx, start_time, end_time for further processing
                for row in doc:
                    row = json.loads(row)
                    source_url = 'https://etherscan.io/tx/' 
                    (item, is_mined) = parse(source_url, row['txhash'])
                    if(is_mined):
                        col_summary.insert(item)
                    print(item) # Debug      
            else:
                try: 
                    # Insert the item to start_time db, ignore the item if duplicate
                    col_end_time.insert(record)
                except:
                    pass
        except:
            pass
            
    return

# mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = mongo_client["transactions"]
# col = db["start_time"]
# col.find({}, no_cursor_timeout=True).limit(30)


# Create a basic configuration
# conf = SparkConf().setAppName("PythonSparkStreamingKafkaEndTimeApp").setMaster("spark://master:7077")
conf = SparkConf().setAppName("PythonSparkStreamingKafkaEndTimeApp")


# Create a SparkContext using the configuration
sc = SparkContext(conf=conf)

# Set log level
sc.setLogLevel("ERROR")

# Set the batch interval in seconds
batch_interval = 2

# Create the streaming contect objects
ssc = StreamingContext(sc,batch_interval)

# Create the kafka connection object
# kafkaStream = KafkaUtils.createStream(ssc, ["starttime"], {"metadata.broker.list": "localhost:9092" ,TRANSACTIONS_DETAILS_TOPIC:1})
kafkaStream = KafkaUtils.createStream(ssc, KAFKA_ZOOKEEPER_CONNECT, "spark-streaming-blocktime", {TRANSACTIONS_TOPIC:1})

lines = kafkaStream.map(lambda x: x[1])

# connect to mongodb
db_connection =  DB()
db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]

col_start_time = db["start_time"]
col_start_time.create_index([('txhash', pymongo.ASCENDING)], unique = True)

col_end_time = db["end_time"]
col_end_time.create_index([('txhash', pymongo.ASCENDING)], unique = True)

col_summary = db["summary"]
col_summary.create_index([('txhash', pymongo.ASCENDING)], unique = True)

# insert data to mongo db
pprint2(lines,col_start_time,col_end_time,col_summary)

# start ssc
ssc.start()
ssc.awaitTermination()


def decoder(msg):
    baseMessage = json.loads(zlib.decompress(msg[4:]))
    message = {"headers": baseMessage["headers"],
               "data": b64decode(baseMessage["data"])}
    return message