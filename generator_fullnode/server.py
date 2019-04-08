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

# def parse_book_link_for_meta_data(bookLink):
#   htmlString = requests.get(bookLink).content
#   bsTree = BeautifulSoup(htmlString,"html.parser")
#   title = bsTree.find("h1", attrs={"id": "bookTitle"}).string
#   author = bsTree.find("a", attrs={"class": "authorName"}).span.string
#   rating = bsTree.find("span", attrs={"itemprop": "ratingValue"}).string
#   description = ''.join(bsTree.find("div", attrs={"id": "description"}).find("span", attrs={"style": "display:none"}).stripped_strings)
#   return dict(title=title.strip() if title else '',author=author.strip() if author else '',rating=float(rating.strip() if rating else 0),description=description)
#
# def parse_and_persist_book_info(bookUrl):
#   redisKey = generate_redis_key_for_book(bookUrl)
#   bookInfo  = parse_book_link_for_meta_data(bookUrl)
#   redisClient.set(redisKey,pickle.dumps(bookInfo))

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
		return "%d txs are scheduled for info parsing."%(len(results))
	return "Only json file of tx hash array is accepted.",400

######################################
## Integrating RQ Dashboard with flask
######################################
app.config.from_object(rq_dashboard.default_settings)
app.config.update(REDIS_URL='redis://redis')
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rqstatus")


if __name__ == '__main__':
	app.run()
