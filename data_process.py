# this script is used to extract gas price and related waiting time
import pandas as pd
import re
import json

# remove substrings before and after two characters
# exmaple:
# input: '12@[123]57'. '[',']'
# output: '[123]'
def remove_redundant_characters(str, char1, char2):
    left_index = str.find(char1)
    right_index = str.find(char2)
    result = str[left_index: (right_index +1)]
    return result
#####################################################################

file = 'test.csv'

dataframe = pd.read_csv(file, names=['time','safe gas','propose gas','pending tx','gas and time'])

#dataframe.columns = ['time','safe gas','propose gas','pending tx','gas and time']
#print(dataframe['time'][0])

for item in dataframe['gas and time']:
    # extract data as string from csv file
    result = re.search(' var _data = (.*) var _sliderData = ', item)
    result = result.group(0)
    result = remove_redundant_characters(result, '[', ']')

    # extract data as json from string
    result = json.loads(result)
    print(result[0]['ID'])
