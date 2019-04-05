import json
import mysql.connector
import requests
import queue
import time

def send_request(url):
  headers = {'content-type': 'application/json'}
  data = '{"method":"parity_pendingTransactions","params":[],"id":1,"jsonrpc":"2.0"}'

  response = requests.post(url,data = data, headers = headers)
  result = response.content
  return result

def get_pendingtransactions(data):
  data = json.loads(data.decode())
  results = []
  if('result' in data):
    txlist = data['result']
    for row in txlist:
      temp = []
      temp.append(row['hash'])
      temp.append(row['gasPrice'])
      temp.append(row['gas'])
      temp.append(0)

      # item = {'hash': row['hash'],'gasprice':row['gasPrice'],'gas':row['gas']}
      # item = {row['hash'],row['gasPrice'],row['gas'],0}
      # results.append(item)
      results.append(temp)

  return results  

# def insert_txlist():
#   return

def main():
  # Create a fifo qeque
  q = queue.Queue() 

  # Setup connection url
  url = 'http://35.162.229.77:8545'
  #url = 'http://localhost:8545'

  # Get response from http request
  data = send_request(url)

  # Extract useful data from request
  start = time.time()
  txlist = get_pendingtransactions(data)
  end = time.time()
  print(end - start, "delay in extracting txlist")
  # print(txlist)

  print("test db connection")

  # DB initialization
  mydb = mysql.connector.connect(
    host = "ethfullnodedb.c0cwkssklnbh.us-west-2.rds.amazonaws.com",
    user = "admin",
    passwd = "l3ft0fth3d0t",
    database = "transactionsdb"
  )

  mycursor = mydb.cursor()
  mycursor.execute("CREATE TABLE IF NOT EXISTS txlist (txhashlist VARCHAR(255) NOT NULL, starttime FLOAT )")
  mycursor.execute("CREATE TABLE IF NOT EXISTS transactions (txhash VARCHAR(255) NOT NULL, gasprice VARCHAR(255) NOT NULL, gas VARCHAR(255), starttime FLOAT)")

  # mycursor.execute("SHOW TABLES")  
  # mycursor.execute("SELECT * FROM txlist")

  # Insert transaction lists into table txlist
  print(txlist, 'txlist')
  sql_insert_query =  "INSERT INTO transactions (txhash, gasprice, gas, starttime) VALUES  (%s, %s, %s,%s)"
  mycursor.executemany(sql_insert_query, txlist)  
  mydb.commit()

  mycursor.execute("SELECT * FROM transactions")

  for x in mycursor:
    print(x)

if __name__== "__main__":
    main()