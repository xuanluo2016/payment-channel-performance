# this script is used to extract gas price and related waiting time
import pandas as pd
import re
import json
import unicodecsv as csv
import pymongo

DEBUG = True

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
#####################################################################


# file = 'data/db.json'
# with open(file, 'r') as f:
#     data = json.load(f)
#     print(data)

# file = "data/db.csv"
# dataframe = pd.read_csv(file, names=['data','time','seconds'])
# for index, row in dataframe.iterrows():
#     print(row['data'])
#     arr = extract_data(row['data'])

# #dataframe.columns = ['time','safe gas','propose gas','pending tx','gas and time']
# data = []

# for index, row in dataframe.iterrows():
#     arr = extract_data(row['gas and time'])
#     for item in arr:
#         temp = {}
#         temp['time'] = row['time']
#         temp['pendingTx'] = row['pending tx']
#         temp['gasPrice'] = item['gasPrice']
#         temp['avgTime'] = item['avgTime']
#         temp['avgTime2'] = item['avgTime2']
#         temp['safeGas'] = row['safe gas']
#         temp['proposeGas'] = row['propose gas']
#         data.append(temp)

# # save the data to local file
# fieldnames = ['time','pendingTx','gasPrice','avgTime','avgTime2', 'safeGas', 'proposeGas']
# write_to_file('data/extracted.csv', fieldnames, data)


# query mongodb for all pending txs
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["transactions"]
col = db["pending"]

if DEBUG:
    doc = col.find({}).limit(1)
else:
    dod = col.find({}
    )

# extrac transaction ids from the collections
for row in doc:
    arr =  json.loads(row['data'])
    arr_hash = arr['result']


count = col.count()
print(count)
