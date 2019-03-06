import requests
import json
from lxml import html
import re

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

    path = '//*[@id="ContentPlaceHolder1_spanGasPrice"]/text()'
    gas_price = get_transaction_detail(parser, path)
    path = '//*[@id="ContentPlaceHolder1_spanGasPrice"]/b/text()'
    gas_price = gas_price + get_transaction_detail(parser, path) 
    path = '//*[@id="ContentPlaceHolder1_spanGasPrice"]/text()[2]'
    gas_price = gas_price + get_transaction_detail(parser, path)


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
    
    path = '//*[@id="ContentPlaceHolder1_spanGasPrice"]/text()'
    gas_price = get_transaction_detail(parser, path)
    path = '//*[@id="ContentPlaceHolder1_spanGasPrice"]/b/text()'
    gas_price = gas_price + get_transaction_detail(parser, path) 
    path = '//*[@id="ContentPlaceHolder1_spanGasPrice"]/text()[2]'
    gas_price = gas_price + get_transaction_detail(parser, path)

    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/text()'
    max_fee = get_transaction_detail(parser, path)
    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/b/text()'
    max_fee = max_fee + get_transaction_detail(parser, path)
    path = '//*[@id="ContentPlaceHolder1_spanTxFee"]/text()[2]'
    max_fee = max_fee + get_transaction_detail(parser, path)

    item = {"txhash": txhash, "time_last_seen": time_last_seen, "time_first_seen": time_first_seen, "gas_limit": gas_limit, "gas_price":gas_price, "max_gas_fee": max_fee }

    return item