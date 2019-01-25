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

// ###############Methods##############################
const WebSocket = require('ws');
const ws = new WebSocket('wss://mainnet.infura.io/ws');
request = ''
ws.on('open', function open() {
  ws.send('{"jsonrpc":"2.0","method":"eth_newPendingTransactionFilter","params":[],"id":1}');
});

ws.on('message', function incoming(data) {
        console.log(data)
    if (request != ''){
        console.log('asking for filter change')
        ws.send(request);
        pausecomp(1000);
    }else{
        console.log('ask for the ')
        // get the filter id
        substr1 = '"result":';
        substr2 = '}';
        id = get_substr(data, substr1, substr2);

        // send request to get pending transactions
        str1 = '{"jsonrpc":"2.0","method":"eth_getFilterChanges","params":[';
        str2 = '],"id":1}';
        request = str1 + id + str2;
        console.log(request)
        ws.send(request);
    }


});