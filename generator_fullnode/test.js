const Web3 = require("web3");

// "Web3.providers.givenProvider" will be set if in an Ethereum supported browser.
// const web3 = new Web3("ws://ec2-35-162-229-77.us-west-2.compute.amazonaws.com:8545");
const web3 = new Web3("ws://localhost:8546");

// const web3 = new Web3("http://35.162.229.77:8545")

web3.eth.subscribe('pendingTransactions', function(error, result) {
    console.log(error);
})
.on('data', function(txData){
    web3.eth.getTransaction(txData).then(console.log);
});
