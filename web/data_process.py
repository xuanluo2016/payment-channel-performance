import requests
import json
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.ticker import PercentFormatter
import statistics as stat

def get_data(url):
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    results = json.loads(response.content.decode())
    return results

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
    plt.legend()
    plt.show()
    return

def plot2D(x,y,*args,**kwargs):
    plt.scatter(x, y,*args, **kwargs)
    plt.legend()
    plt.show()
    return

def create_test_data():
    return

def main():
    urls = ['http://localhost:5000/gasstat','http://localhost:5000/waitingminedtime']
    data = get_data(urls[0])
    # For waiting_mined_time
    # (x,y) = get_data_avg_by_range(data,'_id','value',0.01,500)
    # For waiting_time
    (x,y) = get_data_avg_by_range(data,'_id','value',0.02,10000)
    plot2D(x,y)
    return

if __name__== "__main__":
    main()
