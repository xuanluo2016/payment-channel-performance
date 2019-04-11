const Web3 = require("web3");
var fs = require("fs");


// "Web3.providers.givenProvider" will be set if in an Ethereum supported browser.
// const web3 = new Web3("ws://ec2-35-162-229-77.us-west-2.compute.amazonaws.com:8545");
// const web3 = new Web3("http://35.162.229.77:8545")
const web3 = new Web3("ws://localhost:8546");


web3.eth.subscribe('pendingTransactions', function(error, result) {
    console.log(error);
})
.on('data', function(txData){
    web3.eth.getTransaction(txData).then(function(value) {
       // console.log(value, Math.floor(new Date() / 1000))
       var dict = {};
       dict.data = value
       dict.starttime = Math.floor(new Date() / 1000)	
       fs.writeFile('hello.json', JSON.stringify(dict), 'utf8', function(err) {
       // If an error occurred, show it and return
       if(err) return console.error(err);
       // Successfully wrote to the file!
           });
      })
});
