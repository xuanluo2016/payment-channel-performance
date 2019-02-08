const ReconnectWebSocket = require('./lib/ReconnectWebSocket.js');
const assert = require('assert');

// return substr between two substrings in a string
function get_substr(str, substr1, substr2){
    left = str.indexOf(substr1);
    right = str.indexOf(substr2);
    if(left == -1 || right == -1){
        return '';
    }
    else{
        return str.substring(left + substr1.length,right);
    }
}

function pausecomp(millis)
{
    var date = new Date();
    var curDate = null;
    do { curDate = new Date(); }
    while(curDate-date < millis);
}

// ############### MongoDB ############################## //
// initlaize the mongodb for storing the data
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";
var mongodb;

// Create the database connection
MongoClient.connect(url, {  
    poolSize: 10
    // other options can go here
  },function(err, db) {
      assert.equal(null, err);
      mongodb = db;
      }
  );
// store the data
function insert(query){

    var dbo = mongodb.db("transactions");
    dbo.collection("pending").insertOne(query,function(err, result) {
        assert.equal(null, err);
    });  
}


// ############### WebSocket ############################## //
var request;
url = 'wss://mainnet.infura.io/ws'
// url = 'wss://mainnet.infura.io/_ws'

var wsc = new ReconnectWebSocket();

wsc.open(url)

wsc.onopen = function(e){
    console.log('connected');
    console.log(new Date().toLocaleString());
    this.send('{"jsonrpc":"2.0","method":"eth_newPendingTransactionFilter","params":[],"id":1}');
    request = '';
}
wsc.onmessage = function(data,flags,number){
    //console.log(`WebSocketClient message #${number}: `,data);
    // if the data reports invalid
    if (request != ''){
        //console.log('asking for filter change');
        query = {"data": data, "time": new Date().toLocaleString(), "seconds":Date.now()};
        insert(query)
        this.send(request);
        console.log(new Date().toLocaleString())
        pausecomp(2000);
    }else{
        //console.log('ask for the filter id')
        // get the filter id
        substr1 = '"result":';
        substr2 = '}';
        id = get_substr(data, substr1, substr2);

        // send request to get pending transactions
        str1 = '{"jsonrpc":"2.0","method":"eth_getFilterChanges","params":[';
        str2 = '],"id":1}';
        request = str1 + id + str2;
        console.log(request)
        this.send(request);
    }
}



// const WebSocket = require('./WebSocket.js');
// const WebSocketClient = WebSocket.WebSocketClient;
// var wsc = new WebSocketClient();
// url = 'wss://mainnet.infura.io/ws';
// wsc.open(url);