from lib.db import DB
from lib.string import remove_redundant_characters
from dateutil import parser
import datetime 

DEBUG = True

# extract the minimum time from doc, which contains a field called 'time'
# return None if doc is empty, else return mininum
def get_start_time(doc):
    #min = parser.parse('2039-01-30, 10:38:50 a.m.')
    min = parser.parse(str(datetime.MAXYEAR))
    start_time = min
    try: 
        for row in doc:
            time = row['time']
            time = parser.parse(time)
            if(time < min):
                min = time
    finally: 
        if(start_time == min):
            return None
        else:
            return min

# extract the end time from doc, which contains a field called 'timestamp'
# return None if doc is empty or timestamp is empty, else return timestamp
def get_end_time(doc):
    try:
        for row in doc:
            time = row['timestamp']
            # remove special characters in timestamp
            time = remove_redundant_characters(time, '(', ')')
            time = time[1: len(time)-len("+UTC")-1]
            return time
    except Exception as e:
        return None

####################### Methods #################################

# get the list of transactions and related recording time from db processed
db_connection =  DB()
db = db_connection.mongo_client["transactions"]
col_processed = db["processed"]
col_mined =  db["mined"]

if DEBUG:
    doc = col_processed.find({}).limit(2)
else:
    doc = col_processed.find({})

# extract transaction ids from the collections and remove duplicate transaction hashes
tx_list = []
for row in doc:
    hash = row['txhash']
    if(hash not in tx_list):
        tx_list.append(hash)
    
if DEBUG:
    tx_list.append('0xd98059bbc41c26150d88b4d8cc05ea4d6a609b538e8cdb52aceff3ad04e3cc94')
    tx_list.append('0x2e3adfad08379e8d292c771bca695a941bb9be9142eb7c034bf0859127499b41')
    tx_list.append('0x20aa5435e1ee03778ae85b719f81f334a758468145f8c38b6badbe015ac9cb72')
    tx_list.append('0x7e34ebe793d9e386d278ebeef75192d409066b9e99e2b456b31ca56af7747cbb')
    tx_list.append('0x9bf0ce39118a5bfd65ee1e339b96fe74752fd5dd6ae885a6ed42cab877d70b82')

for tx in tx_list:
    # get the start time of the transactions
    # query = '{txhash : ' + str(tx) + ' }'
    query = {'txhash': tx}
    doc = col_processed.find(query)
    start_time = get_start_time(doc)
    # print('start_time:')
    # print(start_time)

    # get the end time of the transactions
    doc = col_mined.find(query)
    end_time = get_end_time(doc)
    print(tx)
    print('end_time:')
    print(end_time)

    # get the waiting time of the transactions
    if(start_time != None) and (end_time != None):
        waiting_time = end_time - start_time
        print(waiting_time)    


