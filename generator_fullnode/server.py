from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
import pickle
import rq_dashboard
import requests
from bs4 import BeautifulSoup
from lxml import html, etree
import requests
import re
import collections

DEBUG = True
# Use FIFO queue to store a cache of transaction hashcode
MAX_QUEUE_SIZE = 5000
QUEUE = collections.deque(MAX_QUEUE_SIZE)

app = Flask(__name__)

# Spawn a client connection to redis server. Here Docker
# provieds a link to our local redis server usinf 'redis'
redisClient = Redis(host='redis')

# Initialize a redis queue instance with name 'bookInfoParser'.
# This name will be used while declaring worker process so that it can
# start processing tasks in it.
#bookInfoParserQueue = Queue('bookInfoParser',connection=redisClient)
txInfoParserQueue = Queue('txInfoParser',connection=redisClient)
#################################
###### Methods ##################
#################################

# generate_redis_key_for_book = lambda bookURL: 'GOODREADS_BOOKS_INFO:' + bookURL
generate_redis_key_for_tx = lambda txURL: 'TX_INFO:' + txURL


def parse_and_persist_tx_info(requests):
  redisKey = generate_redis_key_for_tx(requests)
  write_data_to_db(requests)
  redisClient.set(redisKey,pickle.dumps(requests))

def write_data_to_db(requests):
	# DB initialization
  ctx = mysql.connector.connect(
      host = "ethfullnodedb.c0cwkssklnbh.us-west-2.rds.amazonaws.com",
      user = "admin",
      passwd = "l3ft0fth3d0t",
      database = "transactionsdb"
  )
  
	# Insert every single transaction into table transadtions
  sql_insert_query =  "INSERT IGNORE INTO txstart (hashcode, txhash, gasprice, gas, starttime) VALUES  (%s, %s, %s, %s,%s)"
  cursor = ctx.cursor()
  cursor.executemany(sql_insert_query, requests)  
  ctx.commit()
	cursor.close()
	ctx.close()
	print("affected rows = {}".format(cursor.rowcount))

# def parse_tx_link_for_meta_data(url):
#     tx_result = ''
#     tx_detailedTime = ''
#     from_address = ''
#     to_address = ''
#     (tx_result, tx_detailedTime, from_address, to_address) = parse_tx(url)
#     if(tx_result == ''):
#         url = re.sub('0x','',url)
#         (tx_result, tx_detailedTime,from_address,to_address) = parse_tx(url)

#     return dict(tx_hash = tx_result, tx_time = tx_detailedTime, takerAddr = from_address, makerAddr = to_address)
#################################
#### ENDPOINTS ##################
#################################

# Health check endpoint - responds if service is healthy
@app.route('/')
def health_check():
	return "Web server is up and running!"

# #Endpoint that accepts an array of tx hashes for querying tx details
# @app.route('/getAllTx', methods=["GET"])
# def get_all_tx_info():
#   result = []
#   txListResult = request.get_json()
#   source_url = SOURCE_URL
#   if (len(txListResult)):
#     for tx_id in txListResult:
#       txURL = source_url + str(tx_id)
#       redisKey = generate_redis_key_for_tx(txURL)
#       cachedValue = redisClient.get(redisKey)
#       if cachedValue:
#         result.append(pickle.loads(cachedValue))
#     return jsonify(result)
#   return "Only array of tx hashes is accepted.",400

# #Endpoint for retrieving book info from Redis
# @app.route('/getTx', methods=["GET"])
# def get_tx_info():
#   txURL = request.args.get('url', None)
#   if (txURL and txURL.startswith('https://www.etherchain.org/tx/')):
#     redisKey = generate_redis_key_for_tx(txURL)
#     cachedValue = redisClient.get(redisKey)
#     if cachedValue:
#       return jsonify(pickle.loads(cachedValue))
#     return "No meta info found for this tx."
#   return "'url' query parameter is required. It must be a valid tx URL.",400

# Endpoint for posting tx ids

@app.route('/parseTx', methods=["POST"])
def parse_tx():
	txListResult = request.get_json()
	requests = []

	# If transaction list is not empty
	if (len(txListResult)):
		for row in txListResult:
			hashcode = row['hashcode']
			if(hashcode not in QUEUE):
				QUEUE.append(hashcode)
				requests.append(row)

	# If any new data, commit data to mysql			
	if(len(requests)):					
			txInfoParserQueue.enqueue_call(func=parse_and_persist_tx_info,args=(requests,),job_id=len(requests))
		return "%d txs are scheduled for info parsing."%(len(requests))
	return "Only json file of tx hash array is accepted.",400

######################################
## Integrating RQ Dashboard with flask
######################################
app.config.from_object(rq_dashboard.default_settings)
app.config.update(REDIS_URL='localhost')
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rqstatus")


if __name__ == '__main__':
	app.run()
