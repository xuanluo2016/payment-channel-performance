import requests
import json
from lxml import html
import re
from datetime import datetime
import dateutil.parser


# get the details of a transaction
def get_transactions(content):
    results = []    
    try: 
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
                datetime = dateutil.parser.parse(start_time)
                epoch = float(datetime.strftime('%s'))

            if(txhash != None) and (start_time != None) and (epoch != None):
                item = {'txhash': txhash, 'starttime': start_time, 'seconds': epoch}
                results.append(item)
    except Exception as e:
        print(e)
        pass
        
    finally:
        return results
