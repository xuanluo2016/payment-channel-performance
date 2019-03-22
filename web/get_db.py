import pymongo
from pymongo.errors import BulkWriteError
from lib.db import DB

from bson import ObjectId, Code
import json
import os

MONGO_INITDB_DATABASE = os.environ.get('MONGO_INITDB_DATABASE')
BATCH_INTERVAL = int(os.environ.get('BATCH_INTERVAL'))

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def get_summary_all():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    doc = col_summary.find()
    results = []
    for row in doc:
        row = JSONEncoder().encode(row)
        results.append(row)
    return results

def get_summary(num):
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    doc = col_summary.find().limit(num)
    results = []
    for row in doc:
        item = {"waiting_time":(row["waiting_time"] + row["waiting_mined_time"]), "actual_cost":row["actual_cost"], "gas_price":row["gas_price"]}
        results.append(item)
    return results

def get_count():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    count_total = col_summary.count()
    count_details = col_summary.count({ '$and': [ {'waiting_time': {'$ne': 0}}, {'actual_cost': {'$ne': 0}} ]})
    return (count_total,count_details)


def get_cost_stat():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]
    query = {'waiting_time': {'$ne': 0.0}, 'actual_cost': {'$ne': 0.0}}

    doc = col_summary.find(query)  

    results = []    
    for row in doc:
        item = {'_id': row['actual_cost'], 'value': (row['waiting_time'] + row['waiting_mined_time'])}
        # row = JSONEncoder().encode(row)
        results.append(item)
    
    return results

def get_cost_avg_stat():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    mapper = Code("""
                function () {
                    emit(this.actual_cost, (this.waiting_time + this.waiting_mined_time));
                }
                """)

    reducer = Code("""
                function(key, values) { return Array.avg(values) }
                """)

    query = {'waiting_time': {'$ne': 0.0}, 'actual_cost': {'$ne': 0.0} }
    doc = col_summary.map_reduce(mapper, reducer, "test_cost", query = query)

    results = []    
    for row in doc.find():
        # row = JSONEncoder().encode(row)
        results.append(row)
    
    return results

def get_cost_median_stat():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    mapper = Code("""
                function () {
                    emit(this.actual_cost, (this.waiting_time + this.waiting_mined_time));
                }
                """)

    reducer = Code("""
                function(key, values) {   
                    values = values.sort(function(a, b){ return a - b; });
                    var i = values.length / 2;
                    return i % 1 == 0 ? (values[i - 1] + values[i]) / 2 : values[Math.floor(i)];
                }
                """)

    query = {'waiting_time': {'$ne': 0.0}, 'actual_cost': {'$ne': 0.0} }
    doc = col_summary.map_reduce(mapper, reducer, "test_cost", query = query)

    results = []    
    for row in doc.find():
        # row = JSONEncoder().encode(row)
        results.append(row)
    
    return results

def get_gas_stat():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]
    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$ne': 0.0}}

    doc = col_summary.find(query)  

    results = []    
    for row in doc:
        item = {'_id': row['gas_price'], 'value': (row['waiting_time'] + row['waiting_mined_time'])}
        # row = JSONEncoder().encode(row)
        results.append(item)
    
    return results

def get_gas_avg_stat():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    mapper = Code("""
                function () {
                    emit(this.gas_price, (this.waiting_time + this.waiting_mined_time));
                }
                """)

    reducer = Code("""
                function(key, values) { return Array.avg(values) }
                """)

    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$ne': 0.0} }
    doc = col_summary.map_reduce(mapper, reducer, "test_gas", query = query)

    results = []    
    for row in doc.find():
        # row = JSONEncoder().encode(row)
        results.append(row)
    
    return results

def get_gas_median_stat():
    # Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    mapper = Code("""
                function () {
                    emit(this.gas_price, (this.waiting_time + this.waiting_mined_time));
                }
                """)

    reducer = Code("""
                function(key, values) {   
                    values = values.sort(function(a, b){ return a - b; });
                    var i = values.length / 2;
                    return i % 1 == 0 ? (values[i - 1] + values[i]) / 2 : values[Math.floor(i)];
                }
                """)

    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$ne': 0.0} }
    doc = col_summary.map_reduce(mapper, reducer, "test_gas", query = query)

    results = []    
    for row in doc.find():
        # row = JSONEncoder().encode(row)
        results.append(row)
    
    return results

def get_avg_mined_time():
    # Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    mapper = Code("""
                function () {
                    emit(this.gas_price, this.waiting_mined_time);
                }
                """)

    reducer = Code("""
                function(key, values) { return Array.avg(values) }
                """)

    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$ne': 0.0} }
    doc = col_summary.map_reduce(mapper, reducer, "test_gas", query = query)

    results = []    
    for row in doc.find():
        # row = JSONEncoder().encode(row)
        results.append(row)
    
    return results

def get_median_mined_time():
    # Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    mapper = Code("""
                function () {
                    emit(this.gas_price, this.waiting_mined_time);
                }
                """)

    reducer = Code("""
                function(key, values) {   
                    values = values.sort(function(a, b){ return a - b; });
                    var i = values.length / 2;
                    return i % 1 == 0 ? (values[i - 1] + values[i]) / 2 : values[Math.floor(i)];
                }
                """)

    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$ne': 0.0} }
    doc = col_summary.map_reduce(mapper, reducer, "test_gas", query = query)

    results = []    
    for row in doc.find():
        # row = JSONEncoder().encode(row)
        results.append(row)
    
    return results

def get_waiting_mined_time():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]
    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$ne': 0.0}}

    doc = col_summary.find(query)  

    results = []    
    for row in doc:
        item = {'_id': row['gas_price'], 'value': (row['waiting_mined_time'])}
        # row = JSONEncoder().encode(row)
        results.append(item)
    
    return results

def get_block_avg_gas():
    # Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    mapper = Code("""
                function () {
                    emit(this.blocknumber, this.gas_price);
                }
                """)

    reducer = Code("""
                function(key, values) { return Array.avg(values) }
                """)

    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$gt': 0.0} }
    doc = col_summary.map_reduce(mapper, reducer, "test_gas", query = query)

    results = []    
    for row in doc.find():
        # row = JSONEncoder().encode(row)
        results.append(row)
    
    return results

def get_block_avg_cost():
    # Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    mapper = Code("""
                function () {
                    emit(this.blocknumber, this.actual_cost);
                }
                """)

    reducer = Code("""
                function(key, values) { return Array.avg(values) }
                """)

    query = {'waiting_time': {'$ne': 0.0}, 'actual_cost': {'$gt': 0.0} }
    doc = col_summary.map_reduce(mapper, reducer, "test_gas", query = query)

    results = []    
    for row in doc.find():
        # row = JSONEncoder().encode(row)
        results.append(row)
    
    return results

def get_block_and_fee():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]
    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$gt': 0.0}}

    doc = col_summary.find(query)  

    results = []    
    for row in doc:
        item = {'_id': row['blocknumber'], 'value': row['gas_price'], 'actual_cost': row['actual_cost'], 'txhash': row['txhash']}
        results.append(item)    
    return results

def get_waiting_time():
# Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]
    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$ne': 0.0}}

    doc = col_summary.find(query)  

    results = []    
    for row in doc:
        item = {'_id': row['gas_price'], 'value': (row['waiting_time'])}
        results.append(item)
    
    return results

def write_to_file(file, results):
    with open(file, 'w') as outfile:
        json.dump(results, outfile)

def update_summary(file):
    data = []
    items = []
    result = 0
    # Get all data 
    with open('data.json') as json_file:  
        data = json.load(json_file)
    json_file.close()

    for row in data:
        row = json.loads(row)
        item = {"txhash": row["txhash"], "blocknumber": row["blocknumber"], "blocktime": row["blocktime"], "waiting_time": row["waiting_time"], "actual_cost": row["actual_cost"], "gas_price": row["gas_price"], "waiting_mined_time": row["waiting_mined_time"]}
        items.append(item)

    if(len(items) > 0):
        # Connect to mongodb
        db_connection =  DB()
        db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
        col_summary = db["summary"]
        try: 
            result = col_summary.insert_many(items, ordered=False)
        except BulkWriteError as bwe:
            pass
    # Return the number of inserted items
    return result

def generate_report(file):
 # Connect to mongodb
    db_connection =  DB()
    db = db_connection.mongo_client[str(MONGO_INITDB_DATABASE)]
    col_summary = db["summary"]

    query = {'waiting_time': {'$ne': 0.0}, 'gas_price': {'$ne': 0.0}}
    doc = col_summary.find(query)
    items = []
    result = 0

    for row in doc:
        start_time = row['blocktime'] - row['waiting_mined_time']
        confirmed_time = row['blocktime'] + row['waiting_time']
        item = {'txhash': row['txhash'], 'start_time': start_time, 'blocktime':row['blocktime'],'confirmed_time':confirmed_time,'gas_price':row['gas_price'],'actual_cost': row['actual_cost']}
        items.append(item)

    if(len(items) > 0):
        col_report = db["report"]
        col_report.create_index([('txhash', pymongo.ASCENDING)], unique = True)
        try: 
            result = col_report.insert_many(items, ordered=False)
        except BulkWriteError as bwe:
            pass
            
    # Close db connection
    col_summary.close()
    col_report.close()

    return result