from lxml import html, etree
import requests
import re
import os
import sys
import argparse
import json
from bs4 import BeautifulSoup
import datetime

DEBUG = True


def parse(source_url, path):
    result = ''
    try:
        print("Fetching gas price details")
        response = requests.get(source_url)
        parser = html.fromstring(response.content)
        result = parser.xpath(path)


        # #print(response.content)
        # #web = urllib.urlopen("http://www.nasdaq.com/quotes/nasdaq-financial-100-stocks.aspx")
        # #pattern = re.compile('var table_body = (.*?);')
        #
        # pattern = re.compile('* var _data = (.*?);')
        # soup = BeautifulSoup(response.content, features='lxml')
        #
        # scripts = soup.find_all('script')
        # for script in scripts:
        #     if (pattern.match(str(script.string))):
        #         data = pattern.match(script.string)
        #         stock = json.loads(data.groups()[0])
        #         print stock

    except Exception as e:
        print("err")
        print(e.message)

    return result

def extract_gas(s):

    return

def extract_tx(str):
    return [int(s) for s in str.split() if s.isdigit()]




if __name__ == "__main__":
    source_url = "https://etherscan.io/gasTracker"
    gasXPath = '/html/body/div[1]/script[4]/text()'
    gasRecords = parse(source_url, gasXPath)

    source_url = "https://etherscan.io/txsPending"
    pendingTxXPath = '/html/body/div[1]/div[4]/div[2]/div[1]/span[2]/text()'
    pendingTxRecords = parse(source_url, pendingTxXPath)

    timeRecords = datetime.datetime.now()
    print(gasRecords)
    print(pendingTxRecords)
    print(timeRecords)

    #### data extraction from raw data ########
    pendingTxNumber = extract_tx(pendingTxRecords[0])[0]
    print(pendingTxNumber)

