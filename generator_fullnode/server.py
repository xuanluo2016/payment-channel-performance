from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
import pickle
import rq_dashboard
import requests
import re
import collections
import mysql.connector

DEBUG = True
# Use FIFO queue to store a cache of transaction hashcode
MAX_QUEUE_SIZE = 15000
QUEUE = collections.deque([],MAX_QUEUE_SIZE)

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
  redisKey = generate_redis_key_for_tx(requests[0][0])
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
  sql_insert_query =  "INSERT IGNORE INTO start (hashcode, txhash, gasprice, gas, starttime, hostname) VALUES  (%s, %s, %s, %s,%s, %s)"
  cursor = ctx.cursor()
  cursor.executemany(sql_insert_query, requests)  
  ctx.commit()
  print("affected rows = {}".format(cursor.rowcount))
  cursor.close()
  ctx.close()

#################################
#### ENDPOINTS ##################
#################################

# Health check endpoint - responds if service is healthy
@app.route('/')
def health_check():
	return "Web server is up and running!"

@app.route('/parseTx', methods=["POST"])
def parse_tx():
	txListResult = request.get_json()
	requests = []

	# If transaction list is not empty
	if (len(txListResult)):
		for row in txListResult:
			# Check if any existing transaction from the server exists
			hashcode = row[0]
			if(hashcode not in QUEUE):
				QUEUE.append(hashcode)
				requests.append(row)

	# If any new data, commit data to mysql			
	if(len(requests)):					
		txInfoParserQueue.enqueue_call(func=parse_and_persist_tx_info,args=(requests,),job_id=str(len(requests)))
		return "%d txs are scheduled for info parsing."%(len(requests))
	return "Only json file of tx hash array is accepted.",400

######################################
## Integrating RQ Dashboard with flask
######################################
app.config.from_object(rq_dashboard.default_settings)
app.config.update(REDIS_URL='redis://resis')
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rqstatus")


if __name__ == '__main__':
	app.run()