import requests
import json
import sys
import matplotlib.pyplot as plt


# get count
url = 'http://localhost:5000/count'
headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
print('number of items in summary: ',int(response.content))

# get summary 
url = 'http://localhost:5000/summary'
headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
results = json.loads(response.content)

print('an example of result:', results[0])
# actual_cost of a transaction
points_x = []

# gas_price of a transaction
points_x2 = []

# waiting_time of a transaction
points_y = []

for row in results:
    points_x.append(row['actual_cost'])
    points_x2.append([row['gas_price']])
    points_y.append(row['waiting_time'])

# Plot
plt.scatter(points_x, points_y)
plt.title('Scatter plot pythonspot.com')
plt.xlabel('number of transaction')
plt.ylabel('number of token types')
plt.show()

# Plot
plt.scatter(points_x2, points_y)
plt.title('Scatter plot pythonspot.com')
plt.xlabel('number of transaction')
plt.ylabel('number of token types')
plt.show()