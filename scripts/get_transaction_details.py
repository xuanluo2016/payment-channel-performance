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


# extract only digits from a string
def extract_digit(str):
    return [int(s) for s in str.split() if s.isdigit()]


source_url = "https://etherscan.io/tx/"
response = requests.get(source_url)
parser = html.fromstring(response.content)
print(parser)
