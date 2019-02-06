# this script is used to extract gas price and related waiting time
import pandas as pd
import re
import json
import unicodecsv as csv
import pymongo
from pymongo.errors import BulkWriteError


# remove substrings before and after two characters
# exmaple:
# input: '12@[123]57'. '[',']'
# output: '[123]'
def remove_redundant_characters(str, char1, char2):
    left_index = str.find(char1)
    right_index = str.find(char2)
    result = str[left_index: (right_index +1)]
    return result

# extract gas and waiting time information from raw data
# input: str by reading csv files
# output: json format data
def extract_data(str):
    # extract data as string from file
    print(str)
    result = re.search('result:(.*)}', str)
    result = result.group(0)  # type: object
    result = remove_redundant_characters(result, '[', ']')

    # extract data as json from string
    result = json.loads(result)
    return result


# write data into file
def write_to_file(file,fieldnames, data):
    with open(file, 'ab')as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
        writer.writeheader()
        try:
            for item in data:
                assert isinstance(item, object)
                writer.writerow(item)
        except Exception as e :
            print("error when writing data to file")
            print(e.message)
    csvfile.close()

def check_duplicate():
    db = mongo_client["transactions"]
    col = db["processed"]
    try: 
        pipeline = [  
            {'$group': { 
                '_id': {'txhash': "$txhash"} 
                } 
            }
        ]
        cursor = col.aggregate(pipeline)
        data = []
        for document in cursor:
            data.append(document['_id']['txhash'])
        
        return(len(data) != len(set(data)))

    except Exception as e:
        print('err in check_duplicate')
    
    return False
#####################################################################

# query mongodb for all pending txs
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["transactions"]
col = db["pending"]
results = []
DEBUG = False

if DEBUG:
    doc = col.find({}).limit(1)
else:
    doc = col.find({}
    )

# extract transaction ids from the collections
for row in doc:
    arr =  json.loads(row['data'])
    if('result' in arr):
        arr_hash = arr['result']
        time = row['time']
        seconds = row['seconds']

        for tx_hash in arr_hash:
            item = {"txhash": tx_hash, "time": time, "seconds": seconds }
            results.append(item)
    
    #print(results)
print("number of items:")
print(len(results))

# store extracted data into mongodb
db = mongo_client["transactions"]
col = db["processed"]
col.create_index([('txhash', pymongo.ASCENDING),('seconds',pymongo.ASCENDING)], unique = True)


try: 
    col.insert_many(results, ordered=False)

except BulkWriteError as bwe:
    # skip duplicate entries
    print("Batch Inserted with some errors. May be some duplicates were found and are skipped.")

except Exception as e:
    print(e.message)

count = col.count()
print(count)

# check if any duplicate entries in the mongodb regarding inserted data
#print(check_duplicate())

