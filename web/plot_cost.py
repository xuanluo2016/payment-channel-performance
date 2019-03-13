import requests
import json
import sys
import matplotlib.pyplot as plt
import seaborn as sns


# get count
url = 'http://localhost:5000/stat'
headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
results = json.loads(response.content)
print('count: ', str(len(results)))
print('an example of result:', results[0])

# actual_cost of a transaction
points_x = []

# waiting_time of a transaction
points_y = []

for row in results:
    points_x.append(row['_id'])
    points_y.append(row['value'])

# get the max of actual cost
print('the max actual cost is: ', str(max(points_x)))

# Plot
plt.scatter(points_x, points_y)
plt.title('Scatter plot')
plt.xlabel('actual cost')
plt.ylabel('waiting time')

plt.xlim(0,0.01)

plt.ylim(0,500)
plt.show()

# # matplotlib histogram
# plt.hist(points_x, color = 'blue', edgecolor = 'black',
#          bins = int(180/5))

# # seaborn histogram
# sns.distplot(points_x, hist=True, kde=False, 
#              bins=int(180/5), color = 'blue',
#              hist_kws={'edgecolor':'black'})
# # Add labels
# plt.title('Histogram of Arrival Delays')
# plt.xlabel('Delay (min)')
# plt.ylabel('Flights')
# plt.show()