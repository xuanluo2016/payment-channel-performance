import requests
import json
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.ticker import PercentFormatter
import statistics as stat
from mpl_toolkits.mplot3d import Axes3D 
from data_process import *

# Get mean least square error
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

def get_lsq_error(func,x_train,y_train):
    popt, pcov = curve_fit(func,x_train, y_train)
    y_prediction = func(x_train, *popt)
    error = rmse(y_prediction,y_train)
    return error

def main():
    # Load the dataset
    urls = ['http://localhost:5000/gasstat','http://localhost:5000/waitingminedtime']
    data = get_data(urls[0])
    
    # Step size
    x = []
    # Sample points
    y = []
    # Least square error
    z = []

    step_size = 0.01

    alpha = 0
    sample = 100
    iter_step_size = 100
    try: 
        while(iter_step_size >= 0):
            cur_step_size = step_size
            cur_sample = sample
            while(True):
                (x_train,y_train) = get_data_avg_by_range(data,'_id','value',cur_step_size,cur_sample)
                
                # # Fit with inverse
                # func = inverse
                # lsq1 = get_lsq_error(func,x_train,y_train)

                # Fit with exponential 
                func = exp
                lsq = get_lsq_error(func,x_train,y_train)

                # Save the lsq error
                x.append(step_size)
                y.append(sample)
                z.append(lsq)
                print('lsq is:',lsq)

                # Start next iteration            
                alpha = alpha + 1
                cur_step_size = step_size*(alpha+1)
                cur_sample = sample *(alpha+1)
                if(alpha >=10):
                    alpha = 0
                    step_size = step_size * 10
                    sample = sample * 10
                    break

            iter_step_size = iter_step_size - 1
    except Exception as e:
        pass

    print(len(x))
    print(len(y))
    print(len(z))
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)

    ax.set_xlabel('step size')
    ax.set_ylabel('sample point')
    ax.set_zlabel('lsq error')

    plt.show()

if __name__== "__main__":
    main()