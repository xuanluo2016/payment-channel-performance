import requests
import json
import sys
import re
import asyncio
import websockets

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
  async with websockets.connect("wss://mainnet.infura.io/ws") as ws:

    # send request to get a new pending transactoin filter id
    request = '{"jsonrpc":"2.0","method":"eth_newPendingTransactionFilter","params":[],"id":1}'
    await ws.send(request)

    # send request too get pending transactions if successfully get a fiilter id
    if True:
      # sample: {"jsonrpc":"2.0","id":1,"result":"0xdc4077b5cc60fae9a6116f165b4e1fc3"}
      result =  await ws.recv()
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
      await ws.send(request)
      if True:
        # sample: {"jsonrpc":"2.0","id":1,"result":"0xdc4077b5cc60fae9a6116f165b4e1fc3"}
        result = await ws.recv()

        # sample: {"jsonrpc":"2.0","id":1,"result":[...]}
        print (result)

    ws.close()

asyncio.get_event_loop().run_until_complete(core())

#
# if __name__ == "__main__":
#   loop = asyncio.get_event_loop()
#   # Blocking call which returns when the hello_world() coroutine is done
#   loop.run_until_complete(core())
#   loop.close()
