from web3 import Web3
import json
from web3.providers.rpc import HTTPProvider
web3 = Web3(HTTPProvider('http://localhost:8545'))
print (web3.eth.blockNumber)
