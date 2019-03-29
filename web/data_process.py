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
                    # arr_y = remove_outlier(arr_y)
                    y.append(np.log(stat.mean(arr_y)))
                    # y.append(stat.mean(arr_y))

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

def create_training_and_test_data(data, scale=0.7):
    total_numer = len(data)
    training_number = int(scale*total_numer)
    data_train = data[:training_number]
    data_test = data[training_number:]
    return(data_train,data_test)

# exponential function
def exp(x, a, b, c,d):
    return a * np.exp(-b *x + c ) + d

def fitFunc(t, A, B, k):
    return A - B*np.exp(-k*t)

def inverse(x, a, b):
    return (a/x) + b 

def fit_curve(x,y, func=inverse,*args, **kwargs):
    x = np.array(x, dtype=float) 
    y = np.array(y, dtype=float)
    
    # Fit curve with inverse function
    popt, pcov = curve_fit(func,x, y)
    # # Fit curve with exp function
    # popt, pcov = curve_fit(exp, x, y)
    # plt.plot(x, exp(x, *popt), 'r--',label='exp: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f' % tuple(popt))

    return (popt, pcov)

def plot_curve_fit(x,y,func,*args, **kwargs):
    popt, pcov = fit_curve(x,y,func)
    plt.plot(x, func(x, *popt), 'b--',label='inverse: a=%5.3f, b=%5.3f' % tuple(popt))
    return

def plot_residual(y,y_prediction):
    plt.scatter(y_prediction, y_prediction - y, c = 'g')
    plt.hlines(y=0, xmin=5, xmax=7)
    plt.title('Residual plot')
    plt.ylabel('Residual')

def rsq(y,y_prediction):
    total_data = len(y_prediction)
    y_avg = np.sum(y)/total_data
    tot_err = np.sum((y - y_avg)**2)
    res_err = np.sum((y - y_prediction)**2)
    r2 = 1 -(res_err/tot_err)
    return r2

def main():
    # Load the dataset
    urls = ['http://localhost:5000/gasstat','http://localhost:5000/waitingminedtime']
    data = get_data(urls[0])
    
    # Split data into training set and test test
    # (x,y) = get_data_avg_by_range(data,'_id','value',0.01,10)
    (data_train,data_test) = create_training_and_test_data(data,0.7)

    # Pre-proces data using step-size
    (x_train,y_train) = get_data_avg_by_range(data_train,'_id','value',0.01,10)
    (x_test, y_test) =  get_data_avg_by_range(data_test,'_id','value',0.01,10)

    # Fit the training data
    plot2D(x_train,y_train, c='g')
    plot_curve_fit(x_train,y_train,inverse)  
    plt.ylabel('total waiting time')
    plt.xlabel('gas price')
    plt.legend()
    plt.show()

    # Use test data to evaluate the fit curve
    popt, pcov = fit_curve(x_train,y_train,inverse)
    y_prediction = inverse(x_test, *popt)

    # Plot test data
    plot2D(x_test,y_test, c='g')
    plt.plot(x_test, y_prediction)
    plt.legend()
    plt.show()

    # plot residual plot using test data
    plot_residual(y_test,y_prediction)
    plt.legend()
    plt.show()

    # Get r-square score  
    print('r square score is: ', rsq(y_test,y_prediction))
if __name__== "__main__":
    main()