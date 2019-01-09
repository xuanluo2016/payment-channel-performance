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

def parse(source_url):
    result = ''
    try:
		print("Fetching gas price details")
		response = requests.get(source_url)
		parser = html.fromstring(response.content)
    except Exception as e :
		print("err")
		print(e.message)

    return result


# def parse_page(parser, results):
# 		# get all transaction ids in the first page
#         # XPATH: /html/body/div[1]/div[5]/div[4]/div/div/div/table/tbody/tr[1]/td[1]/span/a
# 		# XPATH_TX = './/span[@class="address-tag"]'
# 		# txList = parser.xpath(XPATH_TX)
# 		#
# 		# # element = txList[0].xpath('./a/text()')
# 		# # print(element)
# 		# for l in txList:
# 		#     element = l.xpath('./a/text()')
# 		#     txListResult.append(element[0])

# 		# get the maker and taker amount and token name
# 		# XPATH: /html/body/div[1]/div[5]/div[4]/div/div/div/table/tbody/tr[1]/td[3]
# 		#XPATH_PAGEINFO = './/table[@class="table table-hover"]'
# 		XPATH_PAGEINFO = '/html/body/div[1]/div[4]/div[3]/div/div/div/table/tbody/tr'
# 		pageInfo = parser.xpath(XPATH_PAGEINFO)
# 		if(DEBUG):
# 			print("pageInfo")
# 			print(pageInfo)
# 		try:
# 			for info in pageInfo:
# 				# get all transaction id
# 				list = info.xpath('./td[1]/span/a/text()')
# 				result = list[0]
# 				txListResult.append(result)

# 				# get all transaction time
# 				list = info.xpath('./td[2]/span/text()')
# 				result = list[0]
# 				txTime.append(result)

# 				# get all makerBalance
# 				list = info.xpath('./td[3]')
# 				balance = list[0].text
# 				#balance = re.sub('[^0-9]','', balance)
# 				makerBalance.append(balance)

# 				# get all makerTokenAddr
# 				address = list[0].xpath('./a/@href')
# 				address = re.sub('/address/','',str(address[0]))
# 				makerTokenAddr.append(address)

# 				makerTokenName = list[0].xpath('./a/text()')
# 				makerTokenNameList.append(makerTokenName[0])

# 				# get all takerBalance
# 				list = info.xpath('./td[5]')
# 				balance = list[0].text
# 				#balance = re.sub('[^0-9]','', balance)
# 				takerBalance.append(balance)

# 				# get all takerTokenAddr
# 				address = list[0].xpath('./a/@href')
# 				address = re.sub('/address/','',str(address[0]))
# 				takerTokenAddr.append(address)

# 				takerTokenName = list[0].xpath('./a/text()')
# 				takerTokenNameList.append(takerTokenName[0])

# 				# get all price
# 				list = info.xpath('./td[6]')
# 				price = list[0].text
# 				priceList.append(price)
# 		except:
# 			print("err in parse page")

# # get information of makers and takers from pages about transaction details
# def parse_page_details(url,makerAddr,txTime):
# 	response = requests.get(url)
# 	parser = html.fromstring(response.content)

# 	# get the address of makers
# 	# XPATH: //*[@id="ContentPlaceHolder1_maintable"]/div[10]/a
# 	XPATH_MAKERADDR = '//*[@id="ContentPlaceHolder1_maintable"]/div[10]/a/@href'
# 	address = parser.xpath(XPATH_MAKERADDR)
# 	if(len(address) != 0):
# 		address = re.sub('/address/','',str(address[0]))
# 		makerAddr.append(address)

# 	XPATH_TIME = '//*[@id="ContentPlaceHolder1_maintable"]/div[8]/text()'
# 	time = parser.xpath(XPATH_TIME)
# 	print(time)
# 	txTime.append(time)

# # def write_to_file(txListResult, makerAddr, makerBalance, makerTokenAddr,takerBalance,takerTokenAddr):
# # 	with open('%s.csv' % ('maker'), 'wb')as csvfile:
# # 		fieldnames = ['tx hash', 'maker', 'makerBalance',
# # 					  'makerTokenAddr', 'takerBalance', 'takerTokenAddr']
# # 		writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
# # 		writer.writeheader()
# # 		for i in range(0, len(txListResult)):
# # 			try:
# # 				temp = {
# # 					"tx hash": txListResult[i],
# # 					"maker": makerAddr[i],
# # 					"makerBalance": makerBalance[i],
# # 					"makerTokenAddr": makerTokenAddr[i],
# # 					"takerBalance": takerBalance[i],
# # 					"takerTokenAddr": takerTokenAddr[i],
# # 					}
# # 				writer.writerow(temp)
# # 			except:
# # 				f= open("transaction list.txt 111","w+")
# # 				for i in range(1, len(txListResult)):
# # 					f.write("%s\n" %txListResult[i])
# # 				f.close()
# # 				print("error when writing data to file")

# def writePageInfo(parser,txListResult,txTime,makerBalance,makerTokenNameList,takerBalance,takerTokenNameList,makerTokenAddr,takerTokenAddr,priceList):
# 	with open('%s.csv' % ('page'), 'ab')as csvfile:
# 		dir_path = os.path.dirname(os.path.realpath(__file__))
# 		print(dir_path)
# 		fieldnames = ['tx hash', 'tx Time','makerBalance','maker token',
# 					  'makerTokenAddr', 'takerBalance', 'taker token', 'takerTokenAddr', 'price']
# 		writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
# 		#writer.writeheader()
# 		for i in range(0, len(txListResult)):
# 			try:
# 				temp = {
# 					"tx hash": txListResult[i],
# 					"tx Time": txTime[i],
# 					"makerBalance": makerBalance[i],
# 					"maker token": makerTokenNameList[i],
# 					"makerTokenAddr": makerTokenAddr[i],
# 					"takerBalance": takerBalance[i],
# 					"taker token": takerTokenNameList[i],
# 					"takerTokenAddr": takerTokenAddr[i],
# 					"price": priceList[i],
# 					}
# 				writer.writerow(temp)
# 			except:
# 				f= open("tx111.txt","w+")
# 				for i in range(1, len(txListResult)):
# 					f.write("%s\n" %txListResult[i])
# 				f.close()
# 				print("error when writing data to file")
# 	csvfile.close()

# def writePageDetails(txListResult, makerAddr, txTime):
# 	with open('%s.csv' % ('details'), 'wb')as csvfile:
# 		fieldnames = ['tx hash', 'maker', 'txTime']
# 		writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
# 		writer.writeheader()
# 		for i in range(0, len(txListResult)):
# 			try:
# 				temp = {
# 					"tx hash": txListResult[i],
# 					"maker": makerAddr[i],
# 					"txTime": makerBalance[i],
# 					}
# 				writer.writerow(temp)
# 			except:
# 				f= open("tx222.txt","w+")
# 				for i in range(1, len(txListResult)):
# 					f.write("%s\n" %txListResult[i])
# 				f.close()
# 				print("error when writing data to file")


if __name__ == "__main__":
    source_url = "https://etherscan.io/gasTracker"
    gasRecords = parse(source_url)
    timeRecords = datetime.datetime.now()