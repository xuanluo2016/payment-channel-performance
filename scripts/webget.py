import requests
import json
import sys
import re
import asyncio
from websocket import create_connection

# source_url = sys.argv[2]
# print('example: python webget.py data/request/test.json  http://192.168.0.12:5000/')
# r = requests.get(source_url)
# print(r.status_code)
#
# with open(sys.argv[1],'r') as infile:
#     o = json.load(infile)
#     url = source_url + 'getAllTx'
#     headers = {'content-type': 'application/json'}
#     response = requests.get(url, data=json.dumps(o), headers=headers)
#     out = re.sub('request','response',str(sys.argv[1]))
#     #print(response.content)
#     with open(out, 'w') as outfile:
#         #json.dump(response.content, f)
#         outfile.write(response.content)
#     outfile.close()
# infile.close()

# return substr between two substrings in a string
def get_substr(str, substr1, substr2):
  left = str.find(substr1)
  right = str.find(substr2)

  if(left == -1) or (right == -1):
    return ''
  else:
    return str[left+len(substr1):right]

###############Methods##############################

async def core():
  # create web socket connection to infura mainnet
  ws = create_connection("wss://mainnet.infura.io/ws")

  # send request to get a new pending transactoin filter id
  request = '{"jsonrpc":"2.0","method":"eth_newPendingTransactionFilter","params":[],"id":1}'
  ws.send(request)

  # send request too get pending transactions if successfully get a fiilter id
  if True:
    # sample: {"jsonrpc":"2.0","id":1,"result":"0xdc4077b5cc60fae9a6116f165b4e1fc3"}
    result =  ws.recv()
    print ("Received '%s'" % result)

    # get the filter id
    substr1 = '"result":'
    substr2 = '}'
    id = get_substr(result, substr1, substr2)
    print(id)

    # send request to get pending transactions
    str1 = '{"jsonrpc":"2.0","method":"eth_getFilterChanges","params":['
    str2 = '],"id":1}'
    request = str1 + id + str2
    #print(request)
    ws.send(request)
    if True:
      # sample: {"jsonrpc":"2.0","id":1,"result":"0xdc4077b5cc60fae9a6116f165b4e1fc3"}
      result = await ws.recv()
      print (result)

  ws.close()

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  # Blocking call which returns when the hello_world() coroutine is done
  loop.run_until_complete(core())
  loop.close()
