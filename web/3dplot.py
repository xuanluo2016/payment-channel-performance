import requests
import json
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.ticker import PercentFormatter
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# get all
url = 'http://localhost:5000/gasstat3d'

headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
# print(response.content)
results = json.loads(response.content.decode())

print('count: ', str(len(results)))
print('an example of result:', results[0])

# gas_price of a transaction
x = []

# block time of a transaction
y = []

# waiting_time of a transaction
z = []

for row in results:
    gas_price = row['_id']
    block_time =  row['blocktime']
    waiting_time = row['value']

    # if(gas_price <= 50) and (waiting_time <= 500):
    if(gas_price <= float("inf")) and (waiting_time <= float("inf")):
        x.append(gas_price)
        y.append(block_time)
        z.append(waiting_time)

# get the max of actual cost
print('the max gas price is: ', str(max(x)))
print('the min gas price is: ', str(min(x)))
print('the max waiting time is: ', str(max(z)))
print('the min waiting time is: ', str(min(z)))

print(len(x))
print(len(y))
print(len(z))

ax.scatter(x, y, z)

ax.set_xlabel('gas price')
ax.set_ylabel('block time')
ax.set_zlabel('waiting time')

plt.show()