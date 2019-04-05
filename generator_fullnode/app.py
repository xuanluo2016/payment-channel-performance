import json
import mysql.connector
import requests

def insert():
  return

def get_pendingtransactions():
  return

# Setup local connection
url = 'http://localhost:8545'
headers = {'content-type': 'application/json'}
data = '{"method":"parity_pendingTransactions","params":[],"id":1,"jsonrpc":"2.0"}'

response = requests.post(url,data = data, headers = headers)
print(response)


print("test db connection")
mydb = mysql.connector.connect(
  host = "ethfullnodedb.c0cwkssklnbh.us-west-2.rds.amazonaws.com",
  user = "admin",
  passwd = "l3ft0fth3d0t",
  database = "transactionsdb"
)

mycursor = mydb.cursor()


# print(mydb)
# mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE testdb")

# mycursor.execute("SHOW DATABASES")

# for x in mycursor:
#   print(x)
