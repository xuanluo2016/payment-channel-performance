import json
import mysql.connector
import requests
import queue
import time
import threading

# Send request to get pending transactions
def send_request(url):
  headers = {'content-type': 'application/json'}
  data = '{"method":"parity_pendingTransactions","params":[],"id":1,"jsonrpc":"2.0"}'

  response = requests.post(url,data = data, headers = headers)
  result = response.content
  return result

# Extract pending transaction list
def get_pendingtransactions(data, starttime):
  data = json.loads(data.decode())
  results = []
  if('result' in data):
    txlist = data['result']
    for row in txlist:
      temp = []
      temp.append(row['hash'])
      temp.append(row['gasPrice'])
      temp.append(row['gas'])
      temp.append(starttime)
      results.append(temp)

  return results  


def main():
  def worker_push():
      print('worker push started')

      # Setup connection url
      url = 'http://35.162.229.77:8545'
      #url = 'http://localhost:8545'

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
    # DB initialization
    mydb = mysql.connector.connect(
      host = "ethfullnodedb.c0cwkssklnbh.us-west-2.rds.amazonaws.com",
      user = "admin",
      passwd = "l3ft0fth3d0t",
      database = "transactionsdb"
    )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS transactions (txhash VARCHAR(255) PRIMARY KEY, gasprice VARCHAR(255) NOT NULL, gas VARCHAR(255), starttime DOUBLE(50,7), Index(txhash))")
    mydb.commit()

    while True:
      item = q.get()
      if item is None:
        print('no item in the queue')
        break
      # Extract useful data from request
      txlist = get_pendingtransactions(item['data'],item['starttime'])
      print("first entry of transactions:", txlist[0])

      # Insert every single transaction into table transadtions
      sql_insert_query =  "INSERT IGNORE INTO transactions (txhash, gasprice, gas, starttime) VALUES  (%s, %s, %s,%s)"
      # mycursor.execute(sql_insert_query, txlist)  

      mycursor.executemany(sql_insert_query, txlist)  
      mydb.commit()
      print("affected rows = {}".format(mycursor.rowcount))
    
    mydb.close()
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

  # # stop workers
  # for t in threads:
  #     t.join()

if __name__== "__main__":
    main()