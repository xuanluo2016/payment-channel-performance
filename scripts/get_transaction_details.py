from lxml import html
import requests
import datetime
import unicodecsv as csv
from lib.db import DB
import pymongo
import json
from bs4 import BeautifulSoup
import re


DEBUG = True

# get and store details for all input transactions
def parse(source_url,tx_list):
    results = []
    for tx in tx_list:
        # extract transction details
        url = source_url + str(tx)
        item = parse_details(url)

        # store details into array
        if(item != None):
            results.append(item)
    return results

# get the details of a transaction
def parse_details(url):
    result = ''
    try:
        response = requests.get(url)
        parser = html.fromstring(response.content)        

        # check if the transaction has been mined or not
        is_mined = (re.search('Success', response.content) != None)
        if(is_mined):
            # for mined transactions, get TimeStamp, Actual Tx Cost, Gas Limit, Gas Price, Gas Used By Transaction
            result = get_mined_transaction_details(parser)

        else:
            # for unmined transactions, get Time Last Seen, Time First Seen, Gas Limit, Gas Price 
            print('not mined')

    except Exception as e:
        print("err in parse_details")
        print(e.message)

    return result

def get_mined_transaction_details(parser):

    # get TimeStamp
    # list = soup.find('span', id="clock")
    # print(type(list))
    path = '//*[@id="ContentPlaceHolder1_maintable"]/div[8]/text()'
    timestamp = parser.xpath(path)
    print(timestamp)

    actual_cost = ''

    gas_limit = ''

    gas_price = ''

    gas_used = ''
    item = {"timestamp": timestamp, "actual_cost": actual_cost, "gas_limit": gas_limit, "gas_price":gas_price, "gas_used": gas_used }
    

    return

def get_unmined_transaction_details(parse):
    return
####################### Methods #################################

# get the list of transactions from db processed
db_connection =  DB()
db = db_connection.mongo_client["transactions"]
col = db["processed"]

if DEBUG:
    doc = col.find({}).limit(2)
else:
    doc = col.find({})

# extract transaction ids from the collections
tx_list = []
for row in doc:
    hash = row['txhash']
    if(hash not in tx_list):
        tx_list.append(hash)
    
print("number of transctions:")
print(len(tx_list))

if DEBUG:
    tx_list.append('0x9bf0ce39118a5bfd65ee1e339b96fe74752fd5dd6ae885a6ed42cab877d70b82')
    tx_list.append('0xd98059bbc41c26150d88b4d8cc05ea4d6a609b538e8cdb52aceff3ad04e3cc94')

# get the details of trarr_txansaction
source_url = "https://etherscan.io/tx/"
results = parse(source_url, tx_list)
