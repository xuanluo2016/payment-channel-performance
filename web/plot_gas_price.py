import requests
import json
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.ticker import PercentFormatter

# exponential function
def func(x, a, b, c):
    return (-a) * np.exp(-b * x) + c
#   return a * np.log(b * (x)) + c

# inverse function
def inverseFunc(x, a, b):
    return (a*x) + b 

def fitFunc(t, A, B, k):
    return A - B*np.exp(-k*t)

# get all
# url = 'http://localhost:5000/gasstat'
url = 'http://localhost:5000/waitingminedtime'

# get median
# url = 'http://localhost:5000/gasmedian'

# get avg
# url = 'http://localhost:5000/gasavg'

headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
# print(response.content)
results = json.loads(response.content.decode())

print('count: ', str(len(results)))
print('an example of result:', results[0])

# gas_price of a transaction
x = []

# waiting_time of a transaction
y = []

for row in results:
    gas_price = row['_id']
    waiting_time = row['value']
    # if(gas_price <= 50) and (waiting_time <= 500):
    # if(gas_price <= 50) and (waiting_time <= 1000):
    if(gas_price <= float("inf")) and (waiting_time <= float("inf")):
        x.append(gas_price)
        y.append(waiting_time)


# get the max of actual cost
print('the max gas price is: ', str(max(x)))
print('the min gas price is: ', str(min(x)))
print('the max waiting time is: ', str(max(y)))
print('the min waiting time is: ', str(min(y)))

print(len(x))
print(len(y))

# Plot original data
plt.scatter(x, y)

x = np.array(x, dtype=float) 
y = np.array(y, dtype=float)

# Fit curve with exponential
popt, pcov = curve_fit(func, x, y)
plt.plot(x, func(x, *popt), 'b--',label='expoential: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

# Fit curve with inverse
popt, pcov = curve_fit(inverseFunc, x, y)
plt.plot(x, inverseFunc(x, *popt), 'r--',label='inverse: a=%5.3f, b=%5.3f' % tuple(popt))
#Optimization by setting bounds when fitting curve
# popt, pcov = curve_fit(func, x, y, bounds = ((-200,-190),(0,2),(155,160)))
# plt.plot(x, func(x, *popt), 'r--',label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

# Fit with polynomial curve
# m, c = np.polyfit(x, y, 1)
# yn = np.polyval([m, c], x)
# plt.plot(x, yn)

plt.title('Relation between gas price and waiting time')
plt.xlabel('gas price')
plt.ylabel('waiting time')

# # Set ranges of x-axis and y-axis
# plt.xlim(0,50)
# # # # plt.xlim(0.2,0.4)
# plt.ylim(0,500)

plt.legend()
plt.show()

#

# # matplotlib histogram
# plt.hist(x, color = 'blue', edgecolor = 'black',
#          bins = int(180/5))

# # seaborn histogram
# sns.distplot(x, hist=True, kde=False, 
#              bins=int(180/5), color = 'blue',
#              hist_kws={'edgecolor':'black'})

plt.hist(x, weights=np.ones(len(x)) / len(x))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
# Add labels
plt.title('Histogram of gas price')
plt.xlabel('gas price')
plt.ylabel('distribution of gas price')
plt.show()