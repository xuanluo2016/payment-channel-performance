import json
import requests
import queue
import time
import threading
import os
import hashlib

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

def main():
  # Setup connection url
  url = URL
  # Insert complete transaction list into queue
  oldhash = ''
  count = 0
  while True:
      starttime = time.time()
      # Get response from http request
      data = send_request(url)

      # Get new hash values
      hash_object = hashlib.md5(data)
      newhash = hash_object.hexdigest()

      # Transfer byte to string
      data = data.decode()

      if(newhash != oldhash):
          item = {'data':data, 'starttime':starttime, 'hostname': SERVER}
          send_request_to_redis(REDIS_URL,item)
          count = count + 1
          print('pushed items: ', count)
          oldhash = newhash
      endtime = time.time()
      print('lag in time:', endtime - starttime)

if __name__== "__main__":
    main()