import mysql.connector
import config

class DB():
  sql_client = mysql.connector.connect()
  
  def __init__(self):
     self.connect()
   
  def connect(self):
     self.sql_client = mysql.connector.connect(
        host = "ethfullnodedb.c0cwkssklnbh.us-west-2.rds.amazonaws.com",
        user = "admin",
        passwd = "l3ft0fth3d0t",
        database = config.Database
        )
      #mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

  def close(self):
     self.sql_client.close()
   
  def __del__(self):
     self.close()