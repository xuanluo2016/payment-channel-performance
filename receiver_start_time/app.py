import os
# import findspark
# findspark.init('/usr/hdp/2.5.6.0-40/spark')
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

TRANSACTIONS_DETAILS_TOPIC = os.environ.get('TRANSACTIONSTRANSACTIONS_DETAILS_TOPIC_TOPIC')

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.0  pyspark-shell'

# # Create a local StreamingContext
# sc = SparkContext("local[2]","PythonSparkStreamingKafka")

# Create a basic configuration
conf = SparkConf().setAppName("PythonSparkStreamingKafkaApp")

# Create a SparkContext using the configuration
sc = SparkContext(conf=conf)

# Set the batch interval in seconds
batch_interval = 10

# Create the streaming contect objects
ssc = StreamingContext(sc,batch_interval)

# Create the kafka connection object
# kafkaStream = KafkaUtils.createStream(ssc, ["starttime"], {"metadata.broker.list": "localhost:9092" ,TRANSACTIONS_DETAILS_TOPIC:1})

kafkaStream = KafkaUtils.createStream(ssc, "zookeeper:2181", "spark-streaming", {"streaming.transactions.details":1})


lines = kafkaStream.map(lambda x: x[1])
lines.pprint()

ssc.start()
ssc.awaitTermination()

print("everthing is good")

def decoder(msg):
    baseMessage = json.loads(zlib.decompress(msg[4:]))
    message = {"headers": baseMessage["headers"],
               "data": b64decode(baseMessage["data"])}
    return message