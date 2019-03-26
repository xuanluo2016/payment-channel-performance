import os
import json

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import pymongo
from pymongo.errors import BulkWriteError
from lib.db import DB

from get_transaction_details import parse
from get_transaction_summary import get_cost

MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')
TRANSACTIONS_SUMMARY_TOPIC = os.environ.get('TRANSACTIONS_SUMMARY_TOPIC')
KAFKA_ZOOKEEPER_CONNECT = os.environ.get('KAFKA_ZOOKEEPER_CONNECT')
URL = os.environ.get('URL')
BATCH_INTERVAL = int(os.environ.get('BATCH_INTERVAL'))

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.0  pyspark-shell'


def pprint2(lines,col_summary, num=10):
    """
    Print the first num elements of each RDD generated in this DStream.

    @param num: the number of elements from the first will be printed.
    """
    def takeAndPrint(rdd):
        collect = rdd.collect() 
        for record in collect:
            print(record)
            process_record(col_summary, record)

    lines.foreachRDD(takeAndPrint)

def process_record(col_summary,record):
    """
    Check if the txhash exists or not in the end_time table
    if yes, send streaming data to query tx details and remove related record in the end_time db
    else, save data in the start_time db
    """
    record = json.loads(record)
    print('record: ', record)
    print('txhash', record['txhash'])
    if('txhash' in record):
        try: 
            (item, is_mined) = parse(URL, record['txhash'])
            print('item: ', item)
            if(is_mined):
                (actual_cost, gas_price) = get_cost(item)
                print('actual_cost: ', actual_cost)
                print('gas_price: ', gas_price)
        
                if(actual_cost != None) and (gas_price != None):
                    # Update actual cost and gas price in summary collection
                    post = {"actual_cost": actual_cost, "gas_price":gas_price}
                    result = col_summary.update_one({'txhash': record['txhash']},  {'$set': post})
                    print('number of update in summary: ', result.modified_count) # Debug            
       
        except Exception as e:
            print(e)

        finally:
            pass

            
# Create a basic configuration
conf = SparkConf().setAppName("PythonSparkStreamingSummary")

# conf = (SparkConf()
#          .setMaster("spark://master:7077 ")
#          .setAppName("PythonSparkStreamingKafkaApp")
#          .set("spark.executor.memory", "1g"))

# Create a SparkContext using the configuration
sc = SparkContext(conf=conf)

# Set log level
sc.setLogLevel("ERROR")

# Create the streaming contect objects
ssc = StreamingContext(sc,BATCH_INTERVAL)

# Create the kafka connection object
# kafkaStream = KafkaUtils.createStream(ssc, ["starttime"], {"metadata.broker.list": "localhost:9092" ,TRANSACTIONS_DETAILS_TOPIC:1})
kafkaStream = KafkaUtils.createStream(ssc, KAFKA_ZOOKEEPER_CONNECT, "spark-streaming-summary", {TRANSACTIONS_SUMMARY_TOPIC:1})

lines = kafkaStream.map(lambda x: x[1])

# connect to mongodb
db_connection =  DB()
db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]

col_summary = db["summary"]
col_summary.create_index([('txhash', pymongo.ASCENDING)], unique = True)

# insert data to mongo db
pprint2(lines,col_summary)

# start ssc
ssc.start()
ssc.awaitTermination()
