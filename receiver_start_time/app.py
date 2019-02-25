import os
import json

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import pymongo
from lib.db import DB



def pprint2(lines, col,num=10000):
    """
    Print the first num elements of each RDD generated in this DStream.

    @param num: the number of elements from the first will be printed.
    """
    def takeAndPrint(rdd):
        taken = rdd.take(num + 1) 
        try: 
            print("===============================")
            for record in taken[:num]:
                # print(type(record))
                print("***********************************")

                col.insert(json.loads(record))
                # print(col.count())
                print(record)
            if len(taken) > num:
                print("...")
            print("")
        except Exception as e:
            print(e.message)
            pass

    lines.foreachRDD(takeAndPrint)

# mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = mongo_client["transactions"]
# col = db["start_time"]
# col.find({}, no_cursor_timeout=True).limit(30)

TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_ZOOKEEPER_CONNECT = os.environ.get('KAFKA_ZOOKEEPER_CONNECT')

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.0  pyspark-shell'

# Create a basic configuration
conf = SparkConf().setAppName("PythonSparkStreamingKafkaApp")

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
kafkaStream = KafkaUtils.createStream(ssc, KAFKA_ZOOKEEPER_CONNECT, "spark-streaming", {TRANSACTIONS_TOPIC:1})

lines = kafkaStream.map(lambda x: x[1])


# Check if the txhash exists or not in the end_time table
# if yes, send streaming data to query tx details and remove related record in the end_time db
# else, save data in the start_time db

# save data to mongodb
db_connection =  DB()
db = db_connection.mongo_client["transactions"]
col = db["start_time"]

# insert data to mongo db
pprint2(lines,col)



# start ssc
ssc.start()
ssc.awaitTermination()

print("everthing is good")

def decoder(msg):
    baseMessage = json.loads(zlib.decompress(msg[4:]))
    message = {"headers": baseMessage["headers"],
               "data": b64decode(baseMessage["data"])}
    return message