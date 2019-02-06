from lxml import html
import requests
import datetime
import unicodecsv as csv

DEBUG = True

def parse(parser, path):
    result = ''
    try:
        result = parser.xpath(path)

    except Exception as e:
        print("err")
        print(e.message)

    return result


def extract_gas(s):
    return
    
####################### Methods #################################3

source_url = "https://etherscan.io/tx/"
response = requests.get(source_url)
parser = html.fromstring(response.content)
print(parser)
