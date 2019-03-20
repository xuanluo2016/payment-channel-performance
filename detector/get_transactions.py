import requests
import json
from lxml import html
import re


# get the details of a transaction
def get_transactions(content, time):
    parser = html.fromstring(content)
    XPATH_PAGEINFO = '//*[@id="transfers"]/div[2]/table/tbody/tr'
    pageInfo = parser.xpath(XPATH_PAGEINFO)

        for info in pageInfo:
        list = info.xpath('./td[1]/span/a/text()')
        if(len(list) > 0):
                txhash = str(list[0])

        list = info.xpath('./td[3]/span/@title')
        if(len(list) > 0):
                time = list[0]
                start_time = str(time)
                start_time = dateutil.parser.parse(start_time)
                epoch = start_time.strftime('%s')
                
        return(txhash, start_time, epoch)
