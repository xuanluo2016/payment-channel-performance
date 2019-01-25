// return substr between two substrings in a string
function get_substr(str, substr1, substr2){
    left = str.indexOf(substr1);
    right = str.indexOf(substr2);
    console.log(left)
    console.log(right)
    if(left == -1 || right == -1){
        return '';
    }
    else{
        return str.substring(left + substr1.length,right);
    }
}


// ###############Methods##############################


const WebSocket = require('ws');

const ws = new WebSocket('wss://mainnet.infura.io/ws');

ws.on('open', function open() {
  ws.send('{"jsonrpc":"2.0","method":"eth_newPendingTransactionFilter","params":[],"id":1}');
});

ws.on('message', function incoming(data) {
        console.log(data)
    if (data.indexOf('[') !== -1){
        // send request for getting pending transactions filter
        console.log('asking for filter')
        ws.send('{"jsonrpc":"2.0","method":"eth_newPendingTransactionFilter","params":[],"id":1}');

    }else{
        console.log('asking for filter change')
        // send request for getting filter change
        console.log(data);

        // get the filter id
        substr1 = '"result":';
        substr2 = '}';
        id = get_substr(data, substr1, substr2);
        console.log(id);

        // send request to get pending transactions
        str1 = '{"jsonrpc":"2.0","method":"eth_getFilterChanges","params":[';
        str2 = '],"id":1}';
        request = str1 + id + str2;
        ws.send(request);
    }


});

console.log("hello world")