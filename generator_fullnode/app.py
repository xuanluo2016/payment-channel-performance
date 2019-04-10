import json
import requests
import queue
import time
import threading
import os
import hashlib
import config

SERVER = os.uname().nodename
URL = config.URL
REDIS_URL = config.REDIS_URL

# Send request to get pending transactions
def send_request(session,url):
  headers = {'content-type': 'application/json'}
  data = '{"method":"parity_pendingTransactions","params":[],"id":1,"jsonrpc":"2.0"}'

  response = session.post(url,data = data, headers = headers)
  result = response.content
  return result

# Send request to get pending transactions
def send_request_to_redis(session, url, data):
  headers = {'content-type': 'application/json'}
  session.post(url,data = json.dumps(data), headers = headers)
  return 

# Extract pending transaction list
def get_pendingtransactions(data, starttime, results):
  data = json.loads(data)
  # results = []
  if('result' in data):
    txlist = data['result']
    for row in txlist:
      temp = []
      # Generate new hashcode by combining servername and txhash
      hashcode = SERVER+row['hash']
      temp.append(hashcode)
      temp.append(row['hash'])
      temp.append(row['gasPrice'])
      temp.append(row['gas'])
      temp.append(starttime)
      temp.append(SERVER)
      results.append(temp)
  return 
  
def main():
  def worker_push():
    print('worker push started')
    # Setup connection url
    url = URL
    # Insert complete transaction list into queue
    oldhash = ''
    #count = 0
    while True:
        starttime = time.time()
        # Get response from http request
        #data = send_request(url)
        session = requests.Session()
        data = send_request(session, url)

        # Get new hash values
        hash_object = hashlib.md5(data)
        newhash = hash_object.hexdigest()

        # # Transfer byte to string
        # data = data.decode()

        if(newhash != oldhash):
          q.put({'data':data, 'starttime':starttime})
          #count = count + 1
          #print('pushed items: ', count)
          oldhash = newhash
        time.sleep(1)

  def worker_pull():
    print('worker pull started')
    #count = 0
    requests_to_send = []
    max_size = 15000
    session = requests.Session()
    while True:
      try: 
        item = q.get()
        if item is None:
          print('no item in the queue')
          break

        # Extract useful data from request
        get_pendingtransactions(item['data'],item['starttime'],requests_to_send)
        if(len(requests_to_send) >= max_size):
          result = send_request_to_redis(session, REDIS_URL, requests_to_send)
          requests_to_send.clear()
        print('len of queue: ', q.qsize())
      except Exception as e:
        print(e)
        pass
    q.task_done()

  # Create a fifo qeque
  q = queue.Queue(config.QUEUE_MAX_SIZE)
  
  threads = []

  t = threading.Thread(target=worker_push)
  t.start()
  threads.append(t)

  t = threading.Thread(target=worker_pull)
  t.start()
  threads.append(t)

  # block until all tasks are done
  q.join()

#   # stop workers
#   for t in threads:
#       t.join()

if __name__== "__main__":
    main()
