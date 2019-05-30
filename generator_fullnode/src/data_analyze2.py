import requests
import json
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.ticker import PercentFormatter
import statistics as stat
import mysql.connector
import config
from mpl_toolkits.mplot3d import Axes3D
import os
import unicodecsv as csv



def get_db_connection():
    ctx = mysql.connector.connect(
		host = config.Host,
		user = config.User,
		passwd = config.Passwd,
		database = config.Database
	)

    return ctx

# Get the waiting_mined time arranged by starttime
def get_waiting_mined_time():
    ctx = get_db_connection()
    cursor = ctx.cursor()
    x = []
    y = []
    z = []

    # Create view for gathering starttime information
    query = """
        Create or Replace View transactionsdb.txcount AS
        SELECT  count(*) AS count,txhash, min(starttime) As starttime, gasprice FROM transactionsdb.startfromfile
        group by txhash
        """
    cursor.execute(query)
    print("affected rows = {}".format(cursor.rowcount))
    print('refresh view successfully')

    query = """
        select (t2.blocktime - t1.starttime),t1.gasprice, t1.starttime, t1.txhash
        from transactionsdb.txcount as t1, transactionsdb.blocktime as t2
        where t1.txhash = t2.txhash and t1.count = 5
        order by t1.starttime
        """
    cursor.execute(query)
    for row in cursor:
        x.append(row[0])
        y.append(row[1])
        z.append(row[2])

    print(len(x))
    print(len(y))
    print(len(z))

    return x,y,z

# Get the waiting_mined time arranged by starttime
def get_waiting_time():
    ctx = get_db_connection()
    cursor = ctx.cursor()
    x = []
    y = []
    z = []

    # Create view for gathering starttime information
    query = """
        Create or Replace View transactionsdb.txcount AS
        SELECT  count(*) AS count,txhash, min(starttime) As starttime, gasprice FROM transactionsdb.startfromfile
        group by txhash
        """
    cursor.execute(query)
    print("affected rows = {}".format(cursor.rowcount))
    print('refresh view successfully')

    query = """
        select (t2.blocktime - t1.starttime + t3.waitingtime),t1.gasprice, t1.starttime
        from transactionsdb.txcount as t1, transactionsdb.blocktime as t2, transactionsdb.confirmtime as t3
        where t1.txhash = t2.txhash and t1.count = 5 and t2.blocknumber = t3.blocknumber and t1.gasprice < 200
        order by t1.starttime
		limit 100000
        """
    cursor.execute(query)
    for row in cursor:
        x.append(row[0])
        y.append(row[1])
        z.append(row[2])

    print(len(x))
    print(len(y))
    print(len(z))

    return x,y,z

def get_waiting_time2():
    ctx = get_db_connection()
    cursor = ctx.cursor()
    x = []
    y = []
    z = []

    # query = """
    #     select (t2.blocktime - t1.starttime + t3.waitingtime) as waitingtime, t1.gasprice,  t1.starttime,
    #     from db.tabletxcount as t1, db.blocktime as t2, db.confirmtime as t3
    #     where t1.count = 5 and t1.txhash = t2.txhash and t2.blocknumber = t3.blocknumber
    #     order by t1.starttime
    #     """

    query = """
    Select gasprice, (blocktime - starttime + waitingtime), txhash From db.summmaryfromnode1
    """
	#     where blocktime >= 1555027200 and blocktime < 1555200000

    cursor.execute(query)
    for row in cursor:
        x.append(row[0])
        y.append(row[1])

    print(len(x))
    print(len(y))

    return x,y,z

# Get the waiting_mined time arranged by starttime
def get_waiting_time_as_matrix():
    ctx = get_db_connection()
    cursor = ctx.cursor()
    data = []

    # Create view for gathering starttime information
    query = """
        Create or Replace View transactionsdb.txcount AS
        SELECT  count(*) AS count,txhash, min(starttime) As starttime, gasprice FROM transactionsdb.startfromfile
        group by txhash
        """
    cursor.execute(query)
    print("affected rows = {}".format(cursor.rowcount))
    print('refresh view successfully')

    query = """
        select (t2.blocktime - t1.starttime + t3.waitingtime),t1.gasprice, t1.starttime
        from transactionsdb.txcount as t1, transactionsdb.blocktime as t2, transactionsdb.confirmtime as t3
        where t1.txhash = t2.txhash and t1.count = 5 and t2.blocknumber = t3.blocknumber
        order by t1.starttime
        limit 5000000
        """
    # 		limit 100000
    cursor.execute(query)
    for row in cursor:
        temp = {'waitingtime': row[0], 'gasprice': row[1]}
        data.append(temp)
    return data

# Get the waiting_mined time arranged by starttime
def get_waiting_mined_time_from_one_node(hostname):
    ctx = get_db_connection()
    cursor = ctx.cursor()
    x = []
    y = []
    z = []


    query = """
        select (t2.blocktime - t1.starttime),t1.gasprice, t2.blocktime, t1.txhash, t1.starttime
        from transactionsdb.startfromfile as t1, transactionsdb.blocktime as t2
        where t1.txhash = t2.txhash and t1.hostname = '127.0.1.1ip-10-1-2-244'
        order by t1.starttime
        limit 100000
    """
    cursor.execute(query)
    for row in cursor:
        x.append(row[0])
        y.append(row[1])
        z.append(row[2])

    print(len(x))
    print(len(y))
    print(len(z))

    return x,y,z


def get_data(url):
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    results = json.loads(response.content.decode())
    return results

def save_to_csv(file, data):
    return

def get_data_avg_by_range(data,field_x,field_y,range=0,sample=1):
    print('range :', range)
    print('sample: ', sample)
    x = []
    y = []
    # Check the array is not empty and the input targetfield is valid
    if(len(data) > 0) and (field_x in data[0]) and (field_y in data[0]):
        # Sort data by the filter_field in ascending order
        sorted_data = sorted(data, key = lambda i : i[field_x])
        # Get the avg data of other fileds apart from target field by range
        max_value = sorted_data[len(sorted_data) - 1][field_x]
        # Iterate sub lists of data diveded by range and get the average value of each range
        index = 0
        current_x = range
        arr_y = []

        while(current_x <= max_value and index < len(data)):
            temp_x = sorted_data[index][field_x]
            temp_y = sorted_data[index][field_y]
            if(temp_x <= current_x):
                arr_y.append(temp_y)
            else:
                # Save the result only when more than requested samples found in the sublist
                if(len(arr_y) >= sample):
                    x.append(current_x)
                    arr_y = remove_outlier(arr_y)
                    y.append(stat.mean(arr_y))
                # Clear data for current range and start collecting data from next range
                arr_y.clear()
                arr_y.append(temp_y)
                current_x = current_x + range

            index = index + 1
    else:
        print("input list is empty or invalid fields")

    return (x,y)

def get_filtered_data_by_range(data,field_x,field_y,range=0,sample=1):
    print('range :', range)
    print('sample: ', sample)
    x = []
    y = []
    # Check the array is not empty and the input targetfield is valid
    if(len(data) > 0) and (field_x in data[0]) and (field_y in data[0]):
        # Sort data by the filter_field in ascending order
        sorted_data = sorted(data, key = lambda i : i[field_x])
        # Get the avg data of other fileds apart from target field by range
        max_value = sorted_data[len(sorted_data) - 1][field_x]
        # Iterate sub lists of data diveded by range and get the average value of each range
        index = 0
        current_x = range
        arr_y = []

        while(current_x <= max_value and index < len(data)):
            temp_x = sorted_data[index][field_x]
            temp_y = sorted_data[index][field_y]
            if(temp_x <= current_x):
                arr_y.append(temp_y)
            else:
                # Save the result only when more than requested samples found in the sublist
                if(len(arr_y) >= sample):

                    x.append(current_x)
                    arr_y = remove_outlier(arr_y)
                    y.append(stat.mean(arr_y))
                # Clear data for current range and start collecting data from next range
                arr_y.clear()
                arr_y.append(temp_y)
                current_x = current_x + range

            index = index + 1
    else:
        print("input list is empty or invalid fields")

    return (x,y)

def remove_outlier(list):
    mean = stat.mean(list)
    sd = stat.stdev(list)
    final_list = [x for x in list if (x > mean - 2 * sd)]
    final_list = [x for x in final_list if (x < mean + 2 * sd)]
    return final_list

# fields: ["_id", "value"]
def get_data_as_matrix(data, fields):
    m = len(data)
    n = len(fields)

    results = np.zeros((m,n))

    for i in range(0, m) :
        for j in range(0,n):
            results[i][j] = data[i][fields[j]]
    return results

def plot2D_matrix(data,*args,**kwargs):
    plt.scatter(data[:,0], data[:,1],*args, **kwargs)
    return

def plot2D(x,y,*args,**kwargs):
    plt.scatter(x, y,*args, **kwargs)
    return

def create_test_data():
    return



def plot_curve_exp(x,y):

    # exponential function
    def exp(x, a, b, c,d):
        return a * np.exp(-b *x + c ) + d

    def fitFunc(t, A, B, k):
        return A - B*np.exp(-k*t)

    def inverse(x, a, b):
        return (a/x) + b

    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    # Fit curve with inverse function
    popt, pcov = curve_fit(inverse, x, y)
    plt.plot(x, inverse(x, *popt), 'b--',label='inverse: a=%5.3f, b=%5.3f' % tuple(popt))

    # Fit curve with exp function
    popt, pcov = curve_fit(exp, x, y)
    plt.plot(x, exp(x, *popt), 'r--',label='exp: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f' % tuple(popt))

    return

def get_data_within_range(x,y, limit):
    result_x = []
    result_y = []

    for i in range(0,len(x)):
        if(x[i] > limit):
            result_x.append(x)
            result_y.append(y)

    return result_x, result_y


def write_to_csv(x,y):
	with open('%s.csv' % ('samples'), 'ab')as csvfile:
		dir_path = os.path.dirname(os.path.realpath(__file__))
		fieldnames = ['x', 'y']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
		#writer.writeheader()
		for i in range(0, len(x)):
			try:
				temp = {
					"x": x[i],
					"y": y[i],
					}
				writer.writerow(temp)
			except Exception as e:
				print(e)



def main():
    #waiting_mined_time,gasprice,blocktime = get_waiting_mined_time()
    # waiting_mined_time,gasprice,blocktime = get_waiting_time()
    gasprice, waitingtime, txhash= get_waiting_time2()
    # data = get_waiting_time_as_matrix()

    #(waiting_mined_time,gasprice,blocktime) = get_waiting_mined_time_from_one_node('127.0.1.1ip-10-1-2-244')

    # waiting_mined_time with the goes of gas price
    x = gasprice
    y = waitingtime

    write_to_csv(x,y)
    # # Get log of gas price
    # print(type(x[0]))
    # x = np.log(x)
    #
    # # # Get log of waiting mined time
    # # y = y + np.ones(len(y))
    # # y = np.log(y)
    #
    #
    # plt.scatter(x, y)
    # plt.title('Tredency of waiting_mined_time goes with gas price')
    # plt.xlabel('gas price')
    # plt.ylabel('waiting_mined_time')
    # plt.show()

    # # Probability distribution of gas price
    # x2 = np.sort(gasprice)
    # # x2 = np.log(x2)
    # print(max(x2))
    # print(min(x2))
    # y2 = np.arange(len(x2))/float(len(x2))
    # plt.plot(x2, y2)
    # plt.title('Probability distribution of gas price')
    # plt.xlabel('gas price')
    # plt.ylabel('distribution of gas price')
    # plt.show()

    # # Relationship between gasprice, starttime and waiting_mined_time
    # x3 = np.log(gasprice)
    # y3 = blocktime
    # z3 = waiting_mined_time
    # # z3 = z3 + np.ones(len(z3))
    # # z3 = np.log(z3)
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(x3, y3, z3)
    #
    # ax.set_xlabel('gas price')
    # ax.set_ylabel('start time')
    # ax.set_zlabel('waiting mined time')
    #
    # plt.show()

if __name__== "__main__":
    main()
