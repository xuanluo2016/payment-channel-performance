from lxml import html
import requests
import datetime
import unicodecsv as csv
from lib.db import DB
import pymongo
from pymongo.errors import BulkWriteError
import json
from bs4 import BeautifulSoup
import re


DEBUG = True

# get and store details for all input transactions
def parse_all(source_url,tx_list):
    results = []
    for tx in tx_list:
        # extract transction details
        url = source_url + str(tx)
        item, ismined = parse_details(url)

        if(DEBUG):
            print(item)

        # store details into array
        if(item != None):
            results.append(item)
    return results

# get and store details for all input transactions
def parse(source_url,tx):
    url = source_url + str(tx)
    item, is_mined = parse_details(url)
    return (item, is_mined)

# get the details of a transaction
def parse_details(url):
    try:
        response = requests.get(url)
        parser = html.fromstring(response.content)        

        # check if the transaction has been mined or not
        is_mined = (re.search('Success', response.content.decode()) != None)
        if(is_mined):
            # for mined transactions, get TimeStamp, Actual Tx Cost, Gas Limit, Gas Price, Gas Used By Transaction
            item = get_mined_transaction_details(parser)

        else:
            # for unmined transactions, get Time Last Seen, Time First Seen, Gas Limit, Gas Price, Max Fee
            item = get_unmined_transaction_details(parser)
        
        return (item, is_mined)


    except Exception as e:
        print("err in parse_details")
        print(e.message)

    return None

def get_transaction_detail(parser, path):
    result = parser.xpath(path)
    if(result != None and len(result) != 0):
        return result[0]
    else:
        return ''

def get_mined_transaction_details(parser):

    # get TimeStamp
    # list = soup.find('span', id="clock")

    path = '//*[@id="spanTxHash"]/text()'
    txhash = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_maintable"]/div[4]/div[2]/text()[2]'
    timestamp = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/text()'
    actual_cost = get_transaction_detail(parser, path)
    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/b/text()'
    actual_cost = actual_cost + get_transaction_detail(parser, path)
    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/text()[2]'
    actual_cost = actual_cost + get_transaction_detail(parser, path)


    path = '//*[@id="ContentPlaceHolder1_spanGasLimit"]/text()'
    gas_limit = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanGasPrice"]/text()[2]'
    gas_price = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanGasUsedByTxn"]/text()'
    gas_used = get_transaction_detail(parser, path)

    item = {"txhash": txhash, "timestamp": timestamp, "actual_cost": actual_cost, "gas_limit": gas_limit, "gas_price":gas_price, "gas_used": gas_used }
    
    return item

def get_unmined_transaction_details(parser):
    
    path = '//*[@id="spanTxHash"]/text()'
    txhash = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_maintable"]/div[4]/div[2]/span[2]/text()'
    time_last_seen = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_maintable"]/div[5]/div[2]/text()'
    time_first_seen = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanGasLimit"]/text()'
    gas_limit = get_transaction_detail(parser, path) 

    path = '//*[@id="ContentPlaceHolder1_spanGasPrice"]/text()[2]'
    gas_price = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/text()'
    max_fee = get_transaction_detail(parser, path)
    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/b/text()'
    max_fee = max_fee + get_transaction_detail(parser, path)
    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/text()[2]'
    max_fee = max_fee + get_transaction_detail(parser, path)

    item = {"txhash": txhash, "time_last_seen": time_last_seen, "time_first_seen": time_first_seen, "gas_limit": gas_limit, "gas_price":gas_price, "max_gas_fee": max_fee }

    return item
####################### Methods #################################

# get the list of transactions from db processed
db_connection =  DB()
db = db_connection.mongo_client["transactions"]
col = db["processed"]

if DEBUG:
    doc = col.find({}).limit(3)
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


print("number of transctions:")
print(len(tx_list))

# get the details of transactions
source_url = "https://etherscan.io/tx/"
col_mined = db["mined"]
col_mined.create_index([('txhash', pymongo.ASCENDING)], unique = True)

col_unmined = db["unmined"]
col_unmined.create_index([('txhash', pymongo.ASCENDING)], unique = True)

# insert transaction details into mongoDB
for tx in tx_list:
    item, is_mined = parse(source_url, tx)
    try: 

        if(is_mined):
            col_mined.insert(item)
        else:
            col_unmined.insert(item)

    except pymongo.errors.DuplicateKeyError as e:
        print('duplicateKeyError')

    except Exception as e:
        print(e.message)
