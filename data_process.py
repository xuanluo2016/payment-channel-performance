# this script is used to extract gas price and related waiting time
import pandas as pd
import re
import json

file = 'test.csv'
# append header to csv file

# get gas price array at gas and time first
dataframe = pd.read_csv(file)
dataframe.columns = ['time','safe gas','propose gas','pending tx','gas and time']
#print(dataframe['gas and time'])

# get the substring only about gas price and time
#print(dataframe['gas and time'][0])
str = dataframe['gas and time'][0]
result = re.search(' var _data = (.*) var _sliderData = ', str)
substr = result.group(0)
#print(substr)

################################################################
# get all data that matches a pattern
#pattern = 'ID(.*)secs'
pattern = '"gasPrice":(.*),"lastBlock'
result = re.findall(pattern, substr)
# print(result)
# print(len(result))

#####################################################################
# get the json like str
dataframe = pd.read_csv(file)
dataframe.columns = ['time','safe gas','propose gas','pending tx','gas and time']
str = dataframe['gas and time'][0]
result = re.search(' var _data = (.*) var _sliderData = ', str)
substr = result.group(0)
#print(substr)


# clean data by removing unwanted characters -> TODO
left_index = substr.find('[')
right_index = substr.find(']')
substr = substr[left_index: (right_index +1)]
print(substr)


# test the str.find function
# teststr = ' var _data = \'[{"ID":302,"gasPrice":2.0,"lastBlock":7078452,"avgTime":65.0,"avgTime2":"00 hr 01 min 05 secs"},{"ID":295,"gasPrice":3.0,"lastBlock":7078452,"avgTime":63.0,"avgTime2":"00 hr 01 min 03 secs"},{"ID":301,"gasPrice":4.0,"lastBlock":7078452,"avgTime":76.0,"avgTime2":"00 hr 01 min 16 secs"},{"ID":196,"gasPrice":5.0,"lastBlock":7078452,"avgTime":64.0,"avgTime2":"00 hr 01 min 04 secs"},{"ID":303,"gasPrice":6.0,"lastBlock":7078452,"avgTime":66.0,"avgTime2":"00 hr 01 min 06 secs"},{"ID":300,"gasPrice":7.0,"lastBlock":7078452,"avgTime":64.0,"avgTime2":"00 hr 01 min 04 secs"},{"ID":313,"gasPrice":8.0,"lastBlock":7078452,"avgTime":23.0,"avgTime2":"00 hr 00 min 23 secs"},{"ID":182,"gasPrice":9.0,"lastBlock":7078452,"avgTime":55.0,"avgTime2":"00 hr 00 min 55 secs"},{"ID":185,"gasPrice":10.0,"lastBlock":7078452,"avgTime":17610.0,"avgTime2":"04 hr 53 min 30 secs"},{"ID":186,"gasPrice":11.0,"lastBlock":7078452,"avgTime":39.0,"avgTime2":"00 hr 00 min 39 secs"},{"ID":188,"gasPrice":12.0,"lastBlock":7078452,"avgTime":14.0,"avgTime2":"00 hr 00 min 14 secs"}]\';\r\n            var _sliderData = '
# pattern = '['
# print(teststr.find(pattern))
# format a str to json
# substr = json.loads(substr)
# print(substr[0]['ID'])


# read data from json group
data = json.loads(substr)
print(data[0]['gasPrice'])