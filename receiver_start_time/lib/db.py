import pymongo
from pymongo.errors import BulkWriteError

class DB():
   mongo_client =  pymongo.MongoClient()
   
   def __init__(self):
      self.connect()

   def connect(self,url = "mongodb://localhost:27017/"):
      self.mongo_client = pymongo.MongoClient(url)
      #mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

   def close(self):
      self.mongo_client.close()
   
   def __del__(self):
      self.close()