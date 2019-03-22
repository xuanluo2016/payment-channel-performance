import requests
import json
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.ticker import PercentFormatter
from scipy import stats

url = 'http://localhost:5000/blockavggas'
# url = 'http://localhost:5000/blockavgcost'
# url = 'http://localhost:5000/blockandfee'

headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
results = json.loads(response.content.decode())

print('count: ', str(len(results)))
print('an example of result:', results[0])

x = []
y = []

for row in results:
    blocknumber = row['_id']
    avg_fee = row['value']
    x.append(blocknumber)
    y.append(avg_fee)
    if(blocknumber == '0x712a24'):
        print(blocknumber,avg_fee)

print('the max avg gas price is: ', str(max(y)))
print('the min avg gas price is: ', str(min(y)))
print(len(x))
print(len(y))

plt.scatter(x,y)

# fig, axs = plt.subplots(1, 3, sharey=True, tight_layout=True)
plt.title('Relation between block number and gas price')
plt.xlabel('block number')
plt.ylabel('gas price')

# # Plot original data
# axs[0].scatter(x, y, c="g")
# axs[1].hist(x, weights = np.ones(len(x)) / len(x))
# axs[2].hist(y, weights = np.ones(len(y)) / len(y))


plt.legend()
plt.show()

