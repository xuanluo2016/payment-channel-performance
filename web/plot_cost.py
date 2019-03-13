import requests
import json
import sys
import matplotlib.pyplot as plt


# get count
url = 'http://localhost:5000/stat'
headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
results = json.loads(response.content)
print('an example of result:', results[0])
# actual_cost of a transaction
points_x = []

# waiting_time of a transaction
points_y = []

for row in results:
    points_x.append(row['_id'])
    points_y.append(row['value'])

# Plot
plt.scatter(points_x, points_y)
plt.title('Scatter plot')
plt.xlabel('actual cost')
plt.ylabel('waiting time')
plt.xlim(0,0.01)
plt.ylim(0,5000)
plt.show()

