from data_analyze import *

ctx = get_db_connection()
cursor = ctx.cursor()
query = """
Select t1.txhash ,t2.starttime
from transactionsdb.count5tx as t1, transactionsdb.startfromfile as t2
where t1.count =5 and t1.txhash = t2.txhash and t1.txhash in (select txhash from transactionsdb.blocktime)
"""
cursor.execute(query)

txhash_to_mintime = {}
txhash_to_maxtime = {}

# Assign min and max time of a transaction
try: 
    for row in cursor:
        print(row)
        txhash = row[0]
        time = row[1]
        if txhash not in txhash_to_mintime:
            txhash_to_mintime[txhash] = time
            txhash_to_maxtime[txhash] = time
        else:
            if(time < txhash_to_mintime[txhash]):
                txhash_to_mintime[txhash] = time
            if(time > txhash_to_maxtime[txhash]):
                txhash_to_maxtime[txhash] = time
except Exception as e:
    print(e)

cursor.close()   
ctx.close()

# Calculate the difference
min_delta = float('inf')
max_delta = float('-inf')
max_txhash = ''
min_txhash = ''

for txhash, min_time in txhash_to_mintime.items():
    delta = txhash_to_maxtime[txhash] - min_time
    if(delta > max_delta):
        max_delta = delta
        max_txhash = txhash
    if(delta < min_delta):
        min_delta = delta
        min_txhash = txhash

print("max delta is: ", max_delta)
print("txhash of max delta is: ", max_txhash)
print("min delta is: ", min_delta)
print("txhas of min delta is: ", min_txhash)