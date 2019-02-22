
# Import what we need from PySpark
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import os 

import findspark
findspark.init()

# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka_2.1.1:0.8.2.1 pyspark-shell'
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka_2.11:1.6.3  pyspark-shell'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.1  pyspark-shell'

# os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars spark-streaming-kafka-assembly_2.10-1.6.0.jar pyspark-shell' #note that the "pyspark-shell" part is very important!!.

# Create a basic configuration
conf = SparkConf().setAppName("myTestCopyApp")

# Create a SparkContext using the configuration
sc = SparkContext(conf=conf)

print("=========================test================================")

# Set the batch interval in seconds
batch_interval = 10

# Create the streaming contect objects
ssc = StreamingContext(sc,batch_interval)

# Create the kafka connection object
# kafkaStream = KafkaUtils.createStream(ssc, ["starttime"], {"metadata.broker.list": "localhost:9092" ,"streaming.transactions.details":1})

#  kafkaStream = KafkaUtils.createStream(ssc, 'zookeeper:2181', 'spark-streaming', {'streaming.transactions.details':1})
# kafkaStream = KafkaUtils.createDirectStream(ssc, ['streaming.transactions.details'], {"metadata.broker.list": "localhost:9092"})
kafkaStream = KafkaUtils.createStream(ssc, "zookeeper:2181", "spark-streaming", {"streaming.transactions.details":1})
# kafkaStream = KafkaUtils.createStream(ssc, "zookeeper:2181", "spark-streaming", {"streaming.transactions.details":1})

lines = kafkaStream.map(lambda x: x[1])
lines.pprint()

ssc.start()
ssc.awaitTermination()