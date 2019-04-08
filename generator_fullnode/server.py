from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
import pickle
import rq_dashboard
import requests
import re
import collections
import mysql.connector
import json

DEBUG = True

app = Flask(__name__)

# Use FIFO queue to store a cache of transaction hashcode
MAX_QUEUE_SIZE = 5000
QUEUE = collections.deque([],MAX_QUEUE_SIZE)

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

def parse_and_persist_tx_info(results):
  redisKey = generate_redis_key_for_tx(results[0][1])
  write_data_to_db(results)
  redisClient.set(redisKey,pickle.dumps(results))

def write_data_to_db(results):
	print('write_data_to_db')
	# DB initialization
	ctx = mysql.connector.connect(
		host = "ethfullnodedb.c0cwkssklnbh.us-west-2.rds.amazonaws.com",
		user = "admin",
		passwd = "l3ft0fth3d0t",
		database = "transactionsdb"
	)

	# Insert every single transaction into table transadtions
	sql_insert_query =  "INSERT IGNORE INTO start (hashcode, txhash, gasprice, gas, starttime, hostname) VALUES  (%s, %s, %s, %s, %s, %s)"
	cursor = ctx.cursor()
	cursor.executemany(sql_insert_query, results)
	ctx.commit()
	print("affected rows = {}".format(cursor.rowcount))  
	cursor.close()
	ctx.close()

# Extract pending transaction list
def get_pendingtransactions(data, starttime, hostname):
  data = json.loads(data)
  results = []
  if('result' in data):
    txlist = data['result']
    for row in txlist:
      temp = []
      # Generate new hashcode by combining servername and txhash
      hashcode = hostname+row['hash']
      temp.append(hashcode)
      temp.append(row['hash'])
      temp.append(row['gasPrice'])
      temp.append(row['gas'])
      temp.append(starttime)
      temp.append(hostname)
      results.append(temp)

  return results 
#################################
#### ENDPOINTS ##################
#################################

# Health check endpoint - responds if service is healthy
@app.route('/')
def health_check():
	return "Web server is up and running!"

@app.route('/parseTx', methods=["POST"])
def parse_tx():
	print('parse_tx')
	dict_data = json.loads(request.get_json())
	for row in dict_data:
		txListResult = get_pendingtransactions(row['data'], row['starttime'], row['hostname'])
		results = []

		# If transaction list is not empty
		if (len(txListResult)):
			for row in txListResult:
				# 0 stands for hashcode
				hashcode = row[0]
				if(hashcode not in QUEUE):
					QUEUE.append(hashcode)
					results.append(row)

		# If any new data, commit data to mysql	
		if(len(results)):
			print('parseTx')
			txInfoParserQueue.enqueue_call(func=parse_and_persist_tx_info,args=(results,),job_id=str(len(results)))
			print("%d txs are scheduled for info parsing."%(len(results)))
	return

######################################
## Integrating RQ Dashboard with flask
######################################
app.config.from_object(rq_dashboard.default_settings)
app.config.update(REDIS_URL='redis://redis')
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rqstatus")


if __name__ == '__main__':
	app.run()