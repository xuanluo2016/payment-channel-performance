const WebSocket = require('ws');

/**
 * Class representing a WebSocket which reconnects when detecting broken sockets.
 * 
 * @extends WebSocket
 */

class ReconnectWebSocket {
  	/**
	 * Create a new `WebSocket`.
	 * @param {int} number 
	 * @param {int} autoReconnectInterval 
	 */
	constructor (number = 0, autoReconnectInterval = 5*1000) {
		this.number = number;	// Message number
		this.autoReconnectInterval = autoReconnectInterval;	// ms    
	}

	open(url){
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

	send (data,option){
		try{
			this.instance.send(data,option);
		}catch (e){
			this.instance.emit('error',e);
		}
	}

	reconnect(e){
		console.log(`WebSocketClient: retry in ${this.autoReconnectInterval}ms`,e);
			this.instance.removeAllListeners();
		var that = this;
		setTimeout(function(){
			console.log("WebSocketClient: reconnecting...");
			that.open(that.url);
		},this.autoReconnectInterval);
	}


}

ReconnectWebSocket.prototype.onopen = function(e){	console.log("WebSocketClient: open",arguments);	}
ReconnectWebSocket.prototype.onmessage = function(data,flags,number){	console.log("WebSocketClient: message",arguments);	}
ReconnectWebSocket.prototype.onerror = function(e){	console.log("WebSocketClient: error",arguments);	}
ReconnectWebSocket.prototype.onclose = function(e){	console.log("WebSocketClient: closed",arguments);	}
// ReconnectWebSocket.prototype.onreconnect = function(e){	console.log("WebSocketClient: reconnect",arguments);	}

module.exports = ReconnectWebSocket;
