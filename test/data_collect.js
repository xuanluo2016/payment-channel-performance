console.log('test111');

var Web3 = require('web3');

// create an instance of web3 using the HTTP provider.
// NOTE in mist web3 is already available, so check first if it's available before instantiating
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8546"));
console.log(web3);

var version = web3.version;
console.log(version); // "0.2.0"


var number =  web3.eth.getBlockNumber();
console.log(number); // 2744        


console.log('end');