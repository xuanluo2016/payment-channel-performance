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
    if(result == None):
        result = ''
    return result[0]

def get_mined_transaction_details(parser):

    # get TimeStamp
    # list = soup.find('span', id="clock")

    path = '//*[@id="tx"]/text()'
    txhash = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_maintable"]/div[8]/text()'
    timestamp = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/text()[2]'
    actual_cost = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanGasLimit"]/text()'
    gas_limit = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanGasPrice"]/text()[2]'
    gas_price = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanGasUsedByTxn"]/text()'
    gas_used = get_transaction_detail(parser, path)

    item = {"txhash": txhash, "timestamp": timestamp, "actual_cost": actual_cost, "gas_limit": gas_limit, "gas_price":gas_price, "gas_used": gas_used }
    
    return item

def get_unmined_transaction_details(parser):
    
    path = '//*[@id="tx"]/i/font/text()'
    txhash = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_maintable"]/div[6]/span[2]/text()'
    time_last_seen = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_maintable"]/div[8]/span/text()'
    time_first_seen = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanGasLimit"]/text()'
    gas_limit = get_transaction_detail(parser, path) 

    path = '//*[@id="ContentPlaceHolder1_spanGasPrice"]/text()'
    gas_price = get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/text()[2]'
    max_fee = get_transaction_detail(parser, path)

    item = {"txhash": txhash, "time_last_seen": time_last_seen, "time_first_seen": time_first_seen, "gas_limit": gas_limit, "gas_price":gas_price, "max_gas_fee": max_fee }

    return item
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
# tx_list = []
# for row in doc:
#     hash = row['txhash']
#     if(hash not in tx_list):
#         tx_list.append(hash)
    
# print("number of transctions:")
# print(len(tx_list))

# if DEBUG:
#     tx_list.append('0x9bf0ce39118a5bfd65ee1e339b96fe74752fd5dd6ae885a6ed42cab877d70b82')
#     tx_list.append('0xd98059bbc41c26150d88b4d8cc05ea4d6a609b538e8cdb52aceff3ad04e3cc94')

# # get the details of transactions
# source_url = "https://etherscan.io/tx/"
# results = parse_all(source_url, tx_list)

# extract transaction ids from the collections
source_url = "https://etherscan.io/tx/"
col_mined = db["mined"]
col_unmined = db["unmined"]

for row in doc:
    hash = row['txhash']
    item, is_mined = parse(source_url, hash)

    # insert transaction details into mongoDB
    if(is_mined):
        col_mined.insert(item)
    else:
        col_unmined.insert(item)



# if DEBUG:
#     tx_list = []
#     tx_list.append('0x9bf0ce39118a5bfd65ee1e339b96fe74752fd5dd6ae885a6ed42cab877d70b82')
#     tx_list.append('0xd98059bbc41c26150d88b4d8cc05ea4d6a609b538e8cdb52aceff3ad04e3cc94')
#     for tx in tx_list:
#         item, is_mined = parse(source_url, tx)

#         # insert transaction details into mongoDB
#         if(is_mined):
#             col_mined.insert(item)
#         else:
#             col_unmined.insert(item)