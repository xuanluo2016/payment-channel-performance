import requests
import time
import os
import hashlib
import config
import re
import mysql.connector

SERVER = os.uname().nodename
URL = config.URL

def save_to_db(txlist):
    ctx = mysql.connector.connect(
        host = config.Host,
        user = config.User,
        passwd = config.Passwd,
        database = config.Database
    )
    
    cursor = ctx.cursor()
    # Insert every single transaction into table transadtions
    sql_insert_query =  "INSERT IGNORE INTO " + config.Table  + " (hashcode, txhash, gasprice, gas, starttime, hostname) VALUES  (%s, %s, %s, %s,%s, %s)"
    cursor = ctx.cursor()
    cursor.executemany(sql_insert_query, requests)  
    ctx.commit()
    print("affected rows = {}".format(cursor.rowcount))
    cursor.close()
    ctx.close()
    return

# Extract pending transaction list from file
def get_transaction_list(file = 'data-last.json'):
    f = open(file,"r")
    if(f.mode == "r"):
        # Read content of the file line by line
        content = f.read()

        # Seperate files into different lines
        lines = content.split('}')
        results = []
        i = 0
        while(i < len(lines) -1 ):
            temp = extract_data(lines[i], lines[i+1])
            print(temp)
            if(len(temp) == 0):
                results.append(temp)
            i = i + 2

    f.close()
    return results

def extract_data(txdata, time):
    result = []
    if ('hash' in txdata) and ('starttime' in txdata):
        (txhash,gas,gasprice) = extract_transaction_data(txdata)
        starttime = extract_starttime(time)
        hostname = SERVER
        hashcode = hostname+txhash 

        if(txhash != ''):
            result.append(hashcode)
            result.append(txhash)
            result.append(gasprice)
            result.append(gas)
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

def initialize_db_and_table():  

	ctx = mysql.connector.connect(
		host = config.Host,
		user = config.User,
		passwd = config.Passwd,
		database = config.Database
	)

	query = "CREATE TABLE IF NOT EXISTS " + config.Table + " (hashcode VARCHAR(255) PRIMARY KEY, txhash VARCHAR(255) NOT NULL, gasprice VARCHAR(255) NOT NULL, gas VARCHAR(255), starttime DOUBLE(50,7), hostname VARCHAR(255) NOT NULL)"
	cursor.execute(query)
	ctx.commit()
	print("affected rows = {}".format(cursor.rowcount))
	cursor.close()
	ctx.close()
	return
    
def main():

    # initialize db
    initialize_db_and_table()

    # extract transaction list from file
    results = get_transaction_list()
    print('length of results:' ,len(results))
    print('last item in results:' ,results[-1])

    # Insert txlist into mysql
    save_to_db(results)

if __name__== "__main__":
    main()
