import pandas as pd
import re

file = 'test.csv'
# append header to csv file

# get gas price array at gas and time first
dataframe = pd.read_csv(file)
dataframe.columns = ['time','safe gas','propose gas','pending tx','gas and time']
#print(dataframe['gas and time'])

# extract gas price and related waiting time

# get the substring only about gas price and time
#print(dataframe['gas and time'][0])
str = dataframe['gas and time'][0]
result = re.search(' var _data = (.*) var _sliderData = ', str)
substr = result.group(0)
#print(substr)

#extract array of gas an time from substr
result = re.search('\"gasPrice\":(.*),\"lastBlock\"',substr)
print(result.group(0))
