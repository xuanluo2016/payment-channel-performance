import requests
import json
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.ticker import PercentFormatter
from scipy import stats
# get all
# url = 'http://localhost:5000/waitingminedtime'
# url = 'http://localhost:5000/waitingtime'
# url = 'http://localhost:5000/gasstat'

# get avg
url = 'http://localhost:5000/gasavg'
# url = 'http://localhost:5000/minedavg'

headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
# print(response.content)
results = json.loads(response.content.decode())

print('count: ', str(len(results)))
print('an example of result:', results[0])

# gas_price of a transaction
x = []
x_positive = []
x_negative = []
# waiting_time of a transaction
y = []
y_positive = []
y_negative = []

for row in results:
    gas_price = row['_id']
    time = row['value']
    # if(gas_price <= 10) and (time <= 400):
    if(gas_price <= float("inf")) and (time <= float("inf")):
        x.append(gas_price)
        y.append(time)

        if(time > 0):
            x_positive.append(gas_price)
            y_positive.append(time)
        else:
            x_negative.append(gas_price)
            y_negative.append(time)


# get the max of actual cost
print('the max gas price is: ', str(max(x)))
print('the min gas price is: ', str(min(x)))
print('the max time is: ', str(max(y)))
print('the min time is: ', str(min(y)))
print(len(x))
print(len(y))

print('the max gas price is: ', str(max(x_negative)))
print('the min gas price is: ', str(min(x_negative)))

fig, axs = plt.subplots(1, 3, sharey=True, tight_layout=True)
plt.title('Relation between gas price and time')
plt.xlabel('gas price')
plt.ylabel('time')

# Plot original data
axs[0].scatter(x, y, c="g")
axs[1].scatter(x_positive, y_positive, c="r")
axs[2].scatter(x_negative, y_negative, c="b")


plt.legend()
plt.show()
# # Set ranges of x-axis and y-axis
# plt.xlim(0,50)
# # # # plt.xlim(0.2,0.4)
# plt.ylim(0,500)


#

# # matplotlib histogram
# plt.hist(x, color = 'blue', edgecolor = 'black',
#          bins = int(180/5))

# # seaborn histogram
# sns.distplot(x, hist=True, kde=False, 
#              bins=int(180/5), color = 'blue',
#              hist_kws={'edgecolor':'black'})

# plt.hist(y, weights=np.ones(len(y)) / len(y))
# plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
# # Add labels
# plt.title('Histogram of time')
# plt.xlabel('time')
# plt.ylabel('distribution of time')
# plt.show()


# axs[0].hist(x_positive,  weights=np.ones(len(y)) / len(y))

# kolmogrove test
result = stats.ks_2samp(x_positive,x_negative)
print(result)
result = stats.ks_2samp(y_positive,y_negative)
print(result)