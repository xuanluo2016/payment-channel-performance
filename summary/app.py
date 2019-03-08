import pymongo
from pymongo.errors import BulkWriteError
from lib.db import DB
import os
import json
from bson import ObjectId

MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')
BATCH_INTERVAL = int(os.environ.get('BATCH_INTERVAL'))

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def get_data():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    doc = col_summary.find()
    results = []
    for row in doc:
        row = JSONEncoder().encode(row)
        results.append(row)
    
    with open('/data/test/data.json', 'w') as outfile:
        json.dump(results, outfile)

    # mapper = Code("""
    #             function () {
    #                 emit(this.actual_cost, (this.waiting_time + this.waiting_mined_time)); 
    #                 });
    #             }
    #             """)

    # reducer = Code("""
    #                 function (key, values) {
    #                     return Array.avg(values) 
    #                 }
    #                 """)

    # result = db.things.map_reduce(mapper, reducer, "test_mapreduce")
    # for doc in result.find():
    #     pprint.pprint(doc)

get_data()



