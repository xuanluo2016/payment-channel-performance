
##########################################################
# check the length of json files
###########################################################
import json
import sys

with open(sys.argv[1],'r') as f:
    data = json.load(f)
    print(len(data))
