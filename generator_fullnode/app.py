import json
import requests
import queue
import time
import threading
import os

SERVER = os.uname().nodename
URL = 'http://localhost:8545'
REDIS_URL = 'http://70.79.145.26:5000/parseTx'

# Send request to get pending transactions
def send_request(url):
  headers = {'content-type': 'application/json'}
  data = '{"method":"parity_pendingTransactions","params":[],"id":1,"jsonrpc":"2.0"}'

  response = requests.post(url,data = data, headers = headers)
  result = response.content
  return result

# Send request to get pending transactions
def send_request_to_redis(url,data):
  headers = {'content-type': 'application/json'}
  response = requests.post(url,data = json.dumps(data), headers = headers)
  return 

# Extract pending transaction list
def get_pendingtransactions(data, starttime):
  data = json.loads(data.decode())
  results = []
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

  return results 


def main():
  def worker_push():
    print('worker push started')
    # Setup connection url
    url = URL
    # Insert complete transaction list into queue
    oldhash = ''
    count = 0
    while True:
        starttime = time.time()
        # Get response from http request
        data = send_request(url)
        newhash = hash(data)
        if(newhash != oldhash):
          q.put({'data':data, 'starttime':starttime})
          count = count + 1
          print('pushed items: ', count)
          oldhash = newhash
        time.sleep(1)

  def worker_pull():
    print('worker pull started')
  
    while True:
      try: 
        item = q.get()
        if item is None:
          print('no item in the queue')
          break

        # Extract useful data from request
        txlist = get_pendingtransactions(item['data'],item['starttime'])
        print("first entry of transactions:", txlist[0])
        send_request_to_redis(REDIS_URL, txlist)
      except Exception as e:
        print(e)
        pass
    q.task_done()

  # Create a fifo qeque
  q = queue.Queue()
  
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