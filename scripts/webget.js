const WebSocket = require('ws');

function WebSocketClient(){
	this.number = 0;	// Message number
	this.autoReconnectInterval = 5*1000;	// ms
}
WebSocketClient.prototype.open = function(url){
	this.url = url;
	this.instance = new WebSocket(this.url);
	this.instance.on('open',()=>{
		this.onopen();
	});
	this.instance.on('message',(data,flags)=>{
		this.number ++;
		this.onmessage(data,flags,this.number);
	});
	this.instance.on('close',(e)=>{
		switch (e.code){
		case 1000:	// CLOSE_NORMAL
			console.log("WebSocket: closed");
			break;
		default:	// Abnormal closure
			this.reconnect(e);
			break;
		}
		this.onclose(e);
	});
	this.instance.on('error',(e)=>{
		switch (e.code){
		case 'ECONNREFUSED':
			this.reconnect(e);
			break;
		default:
			this.onerror(e);
			break;
		}
	});
}
WebSocketClient.prototype.send = function(data,option){
	try{
		this.instance.send(data,option);
	}catch (e){
		this.instance.emit('error',e);
	}
}
WebSocketClient.prototype.reconnect = function(e){
	console.log(`WebSocketClient: retry in ${this.autoReconnectInterval}ms`,e);
        this.instance.removeAllListeners();
	var that = this;
	setTimeout(function(){
		console.log("WebSocketClient: reconnecting...");
		that.open(that.url);
	},this.autoReconnectInterval);
}
WebSocketClient.prototype.onopen = function(e){	console.log("WebSocketClient: open",arguments);	}
WebSocketClient.prototype.onmessage = function(data,flags,number){	console.log("WebSocketClient: message",arguments);	}
WebSocketClient.prototype.onerror = function(e){	console.log("WebSocketClient: error",arguments);	}
WebSocketClient.prototype.onclose = function(e){	console.log("WebSocketClient: closed",arguments);	}

///////////////////////////////////////////////////////////////////
var assert = require('assert');

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

function setupWebSocket(){
    //initlize the websocket 
    var wsc = new WebSocketClient();
    wsc.open('wss://mainnet.infura.io/ws');
    //wsc.open(' wss://mainnet.infura.io/_ws');
    var request;

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

}
// ###############Methods##############################
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

// start to connect to ws server and collect data
setupWebSocket()


