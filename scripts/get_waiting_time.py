from lib.db import DB
from dateutil import parser

DEBUG = True

# extract the minimum time from doc, which contains a field called 'time'
def get_min_time(doc):
    if(doc == None):
        return None

    min = parser.parse('2019-01-30, 10:38:50 a.m.')
    for row in doc:
        time = row['time']
        time = parser.parse(time)
        if(time < min):
            time = min
    return min
####################### Methods #################################


# get the list of transactions and related recording time from db processed
db_connection =  DB()
db = db_connection.mongo_client["transactions"]
col = db["processed"]

if DEBUG:
    doc = col.find({}).limit(2)
else:
    doc = col.find({})

# extract transaction ids from the collections and remove duplicate transaction hashes
tx_list = []
for row in doc:
    hash = row['txhash']
    if(hash not in tx_list):
        tx_list.append(hash)
    
if DEBUG:
    tx_list.append('0x9bf0ce39118a5bfd65ee1e339b96fe74752fd5dd6ae885a6ed42cab877d70b82')
    tx_list.append('0xd98059bbc41c26150d88b4d8cc05ea4d6a609b538e8cdb52aceff3ad04e3cc94')
    tx_list.append('0x2e3adfad08379e8d292c771bca695a941bb9be9142eb7c034bf0859127499b41')
    tx_list.append('0x20aa5435e1ee03778ae85b719f81f334a758468145f8c38b6badbe015ac9cb72')
    tx_list.append('0x7e34ebe793d9e386d278ebeef75192d409066b9e99e2b456b31ca56af7747cbb')

print(tx_list)
for tx in tx_list:
    # get the start time of the transactions
    # query = '{txhash : ' + str(tx) + ' }'
    query = {'txhash': tx}
    doc = col.find(query)
    start_time = get_min_time(doc)
    print(start_time)
    # get the end time of the transactions

    # get the waiting time of the transactions
        


