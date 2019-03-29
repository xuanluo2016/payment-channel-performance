import requests
import json
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.ticker import PercentFormatter
from scipy.stats import ks_2samp

# get all
url = 'http://localhost:5000/waitingminedtime'
# url = 'http://localhost:5000/waitingtime'
# url = 'http://localhost:5000/gasstat'

# get avg
# url = 'http://localhost:5000/gasavg'
# url = 'http://localhost:5000/minedavg'

# get median
# url = 'http://localhost:5000/gasmedian'

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
count = 0
x_negative = []
y_negative = []

for row in results:
    gas_price = row['_id']
    time = row['value']

    # if(gas_price <= 50) and (time > 0):
    # if(gas_price <= 10):
    # if(gas_price <= 50):
    if(gas_price <= float("inf")) and (time <= float("inf")):
        if(time <= 0):
            count = count + 1
            x_negative.append(gas_price)
            y_negative.append(time)
        else:
            x.append(gas_price)
            y.append(time)

# plt.hist(x_negative, weights=np.ones(len(x_negative)) / len(x_negative))
# plt.title('Relation between gas price and time when time is negative')
# plt.xlabel('gas price')
# plt.ylabel('time')
# plt.legend()
# plt.show()

ks_result = ks_2samp(x,x_negative)
print(ks_result)