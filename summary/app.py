import pymongo
from pymongo.errors import BulkWriteError
from lib.db import DB
from time import sleep
import os

MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')
BATCH_INTERVAL = int(os.environ.get('BATCH_INTERVAL'))

def get_data():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]
    print('test')

get_data()

