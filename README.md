# Data analysis of Ethereum transaction waiting time

This is a system model to explore the relationship between the number of pending transactions, gas price and estimated waiting time in live Ethereum network.  The implementation consists of three steps:

### Data collection
```
python data_crawl.py
```
### Data Modelling
###### Data Visualization


### Application of the data model



### Setup
Clone the repo and run `npm install`. You will need truffle installed globally

### Compatible versions:
```
web3: 1.0.0-beta.37
npm: 6.6
nodejs: 10.15.0
```
### Install dependent packages
```
npm i web3
npm i web-utils
npm i sleep
npm i await-transaction-mined
npm i truffle-assertions
npm i truffle-test-utils
npm i random-number

```


### Compile & migrate
```
truffle compile
truffle migrate
```

### Run tests
Make sure you have testrpc running and listening on port 8545
```
truffle test
```


