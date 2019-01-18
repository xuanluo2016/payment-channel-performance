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
left_index = str.find('[')
right_index = str.find(']')
substr = substr[left_index: right_index]
print(substr)

# format a str to json
teststr = '[{"ID":302,"gasPrice":2.0,"lastBlock":7078452,"avgTime":65.0,"avgTime2":"00 hr 01 min 05 secs"},{"ID":295,"gasPrice":3.0,"lastBlock":7078452,"avgTime":63.0,"avgTime2":"00 hr 01 min 03 secs"}]'
testdata = json.loads(teststr)
print(testdata[0]['ID'])


# read data from json group