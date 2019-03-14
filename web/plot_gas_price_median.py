import requests
import json
import sys
import matplotlib.pyplot as plt
import seaborn as sns


# get count
url = 'http://localhost:5000/gasmedian'
headers = {'content-type': 'application/json'}
response = requests.get(url, headers=headers)
results = json.loads(response.content)

print('count: ', str(len(results)))
print('an example of result:', results[0])

# gas_price of a transaction
points_x = []

# waiting_time of a transaction
points_y = []

for row in results:
    points_x.append(row['_id'])
    points_y.append(row['value'])

# get the max of actual cost
print('the max gas price is: ', str(max(points_x)))
print('the min gas price is: ', str(min(points_x)))
print('the max waiting time is: ', str(max(points_y)))
print('the min waiting time is: ', str(min(points_y)))

print(len(points_x))
print(len(points_y))

# Plot
plt.scatter(points_x, points_y)
# plt.title('Scatter plot')
# plt.xlabel('gas price')
# plt.ylabel('waiting time')

plt.xlim(0,50)
# # # plt.xlim(0.2,0.4)

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