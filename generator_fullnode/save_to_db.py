import requests
import time
import os
import hashlib
import config
import re

SERVER = os.uname().nodename
URL = config.URL
REDIS_URL = config.REDIS_URL

# Extract pending transaction list from file
def save_to_db(file = 'data.json'):
    f = open(file,"r")
    if(f.mode == "r"):
        # Read content of the file line by line
        content = f.read()

        # Seperate files into different lines
        lines = content.split('}')
        results = []
        length = len(lines)
        for i in range(0, int(length/2)):
            temp = extract_data(lines[i], lines[i+1])
            results.append(temp)

    f.close()
    print(results)
    return results

def extract_data(txdata, time):
    result = []

    (txhash,gas,gasprice) = extract_transaction_data(txdata)
    starttime = extract_starttime(time)
    hostname = SERVER
    
    result.append(txhash)
    result.append(gas)
    result.append(gasprice)
    result.append(starttime)
    result.append(hostname)

    return result

def extract_transaction_data(txdata):
    # Find substring of txhash
    txhash = find_between(txdata, 'hash', ',')
    # Remove all special characters between ' and '
    txhash = find_between(txhash, "'", "'")

    # Find substr of gas
    gas = find_between(txdata, 'gas', ',')
    # Remove all special characters
    gas = re.sub(':','',gas)
    gas = re.sub(' ','',gas)
    # Transform gas to float format
    gas = float(gas)

    # Find substr of gas price
    gasprice = find_between(txdata, 'gasPrice', ',')
    # Remove all special characters between ' and '
    gasprice = find_between(gasprice, "'", "'")
    # Transform gasprice to float format
    gasprice = float(gasprice)/1000000000

    return (txhash,gas,gasprice)

def extract_starttime(time):
    
    # Find substr of starttime
    starttime = find_after(time, 'starttime')

    # Remove all special characters
    starttime = re.sub(':','',starttime)
    starttime = re.sub(' ','',starttime)
    # Transform gas to float format
    starttime = float(starttime)
    return starttime

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]

    except ValueError:
        return ""

def find_after( s, first):
    try:
        start = s.index( first ) + len( first )
        end = len(s)
        return s[start:end]

    except ValueError:
        return ""

def test(file = 'data.json'):
    with open(file) as f:
        lines = f.read().splitlines()
        for line in lines:
            print(line)

def test2(file = 'data.json'):
    with open(file) as f:
        content = f.read()
        lines = content.split('}')
        for line in lines:
            print(line)

def main():
    save_to_db()
    #test()
    # test2()

if __name__== "__main__":
    main()
