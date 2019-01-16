from lxml import html, etree
import requests
import re
import os
import sys
import argparse
import json
from bs4 import BeautifulSoup
import datetime
import os
import unicodecsv as csv

DEBUG = True


def parse(parser, path):
    result = ''
    try:
        # print("Fetching gas price details")
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


# extract only digits from a string
def extract_digit(str):
    return [int(s) for s in str.split() if s.isdigit()]


def writePageInfo(file,timeRecord,safeGasRecord,proposeGasRecord, pendingTxNumber):
	with open(file, 'ab')as csvfile:
		fieldnames = ['time', 'safe gas','propose gas','pending tx']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
		#writer.writeheader()
		try:
			temp = {
				"time": timeRecord,
				"safe gas": safeGasRecord,
				"propose gas": proposeGasRecord,
				"pending tx":pendingTxNumber,
			}
			writer.writerow(temp)
		except Exception as e :
			print("error when writing data to file")
			print(e.message)
	csvfile.close()



if __name__ == "__main__":
    source_url = "https://etherscan.io/gasTracker"
    response = requests.get(source_url)
    parser = html.fromstring(response.content)

    # get the array of estimated gas and prices
    gasXPath = '/html/body/div[1]/script[4]/text()'
    gasRecords = parse(parser, gasXPath)

    # get the safe gas price
    safeGasXPath = '//*[@id="ContentPlaceHolder1_ltGasPrice"]/text()'
    safeGasRecord = parse(parser, safeGasXPath)[0]
    print(safeGasRecord)

    # get the propose gas price
    proposeGasXPath = '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/ul/li[3]/div/span/text()'
    proposeGasRecord = parse(parser, proposeGasXPath)
    proposeGasRecord = extract_digit(proposeGasRecord[0])[0]
    print(proposeGasRecord)

    # get the pending tx number
    source_url = "https://etherscan.io/txsPending"
    response = requests.get(source_url)
    parser = html.fromstring(response.content)
    pendingTxXPath = '/html/body/div[1]/div[4]/div[2]/div[1]/span[2]/text()'
    pendingTxNumber = parse(parser, pendingTxXPath)

    pendingTxRecord = extract_digit(pendingTxNumber[0])[0]
    print(pendingTxRecord)

    # get curent time
    timeRecords = datetime.datetime.now()
    print(timeRecords)


    #data = {"c" :0, "b":0}
    data = {}
    data['safe gas'] = safeGasRecord
    data['propose gas'] = proposeGasRecord
    data['pending tx'] = pendingTxRecord
    #data['gas and time'] = gasRecords
    data['time'] = timeRecords.isoformat()

    # data.append(proposeGasRecord)
    # data.append(pendingTxRecord)
    # data.append(gasRecords)
    # data.append(timeRecords)
    # data['test'] = []
    # data['test'].append(dict(time=timeRecords.isoformat(), safegas=safeGasRecord))
    #

    # data['safe gas'] = []
    # data['safe gas'].append(safeGasRecord)
    #
    # data['propose gas'] = []
    # data['propose gas'].append(proposeGasRecord)
    #
    # data['pending tx'] = []
    # data['pending tx'].append(pendingTxRecord)
    #
    # data['gas and time'] = []
    # data['gas and time'].append(gasRecords)
    #
    # data['time'] = []
    # data['time'].append(timeRecords.isoformat())


    file = 'data.csv'
    try:
        #writePageInfo(file, timeRecords.isoformat(), safeGasRecord, proposeGasRecord, pendingTxRecord)
        writePageInfo(file, data['time'],  data['safe gas'], data['propose gas'], data['pending tx'])
    except Exception as e:
        print("error when writing data to file")
        print(e.message)