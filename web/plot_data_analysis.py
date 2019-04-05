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
    try: 
        popt, pcov = curve_fit(func,x_train, y_train)
        y_prediction = func(x_train, *popt)
        error = rmse(y_prediction,y_train)
        return error
    except Exception as e:
        print(e)
        return None

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
    baby_step = 0.01

    sample = 100
    baby_sample = 100
    iter_step_size = 100
    count = 0
    
    while(iter_step_size >= 0):
        step_size = step_size + baby_step
        sample = baby_sample
        iter_sample = 100
        while(iter_sample >= 0):
            sample = sample + baby_sample
            (x_train,y_train) = get_data_avg_by_range(data,'_id','value',step_size,sample)

            # Fit with exponential 
            func = exp
            lsq = get_lsq_error(func,x_train,y_train)

            if(lsq != None):
                # Save the lsq error
                x.append(step_size)
                y.append(sample)
                z.append(lsq)
                print('lsq is:',lsq)
                
            iter_sample = iter_sample -1

        iter_step_size = iter_step_size - 1

    
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