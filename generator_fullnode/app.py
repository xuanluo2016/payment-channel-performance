from web3 import Web3
import json
from web3.providers.rpc import HTTPProvider
import mysql.connector

web3 = Web3(HTTPProvider('http://localhost:8545'))
print (web3.eth.blockNumber)
print (web3.eth.syncing)
print (web3.txpool.inspect)

print("test db connection")
mydb = mysql.connector.connect(
  host = "ethfullnodedb.c0cwkssklnbh.us-west-2.rds.amazonaws.com",
  user = "admin",
  passwd = "l3ft0fth3d0t"
)

print(mydb)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE testdb")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)
