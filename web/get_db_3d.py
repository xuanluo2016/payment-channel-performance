import pymongo
from pymongo.errors import BulkWriteError
from lib.db import DB

from bson import ObjectId, Code
import json
import os

MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')
BATCH_INTERVAL = int(os.environ.get('BATCH_INTERVAL'))

def get_gas_stat_3d():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]
    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$ne': 0.0}}

    doc = col_summary.find(query)  

    results = []    
    for row in doc:
        item = {'_id': row['gas_price'], 'value': (row['waiting_time'] + row['waiting_mined_time']), 'blocktime': row['blocktime']}
        results.append(item)
    
    return results
