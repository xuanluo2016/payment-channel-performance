# this script is used to visualize data for future modelling reference
import pandas as pd
import re

import math
#import numpy as np
#import matplotlib.pyplot as plt
from data_process import write_to_file

file = 'data/extracted.csv'
dataframe = pd.read_csv(file)

result = []
for index, row in dataframe.iterrows():
    str1 = row['gasPrice']
    str2 = row['safeGas']

    print(str1)
    index = str1.find('0')
    str1 = str1[:(index -1)]
    print(str1)

    #if int(float(row['gasPrice'])) == row['safeGas']:
    if str1 == str2:
        result.append(row)

# save the data to local file
fieldnames = ['time', 'pendingTx', 'gasPrice', 'avgTime', 'avgTime2', 'safeGas', 'proposeGas']
write_to_file('data/extracted-safegas.csv', fieldnames, result)


# get data where safe gas is equal to gas price
# result = []
# print(len(dataframe))
# for i in range(1, len(dataframe)):
#     if(dataframe[i]['gasPrice'] ==  dataframe[i]['safeGas']):
#         result.append(dataframe[i])
#
# # save the data to local file
# fieldnames = ['time','pendingTx','gasPrice','avgTime','avgTime2', 'safeGas', 'proposeGas']
# write_to_file('data/extracted-safegas.csv', fieldnames, result)
#


# generate data points
# x = pendingTx, y = gasPrice, z = aveTime
# a potential parameter: time.  In case future state may have a dependency on previous states. In which case, a time-series model then.




