from lxml import html
import requests
import datetime
import unicodecsv as csv
from lib.db import DB

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

####################### Methods #################################

# get the list of transactions from db
db_connection =  DB()
db = db_connection.mongo_client["transactions"]


source_url = "https://etherscan.io/tx/"
response = requests.get(source_url)
parser = html.fromstring(response.content)
