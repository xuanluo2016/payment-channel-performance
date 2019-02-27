from websocket import create_connection

def get_transactions_from_block(url, query):
    ws = create_connection(url)
    # print("Sending 'Hello, World'...")
    # print(query)
    ws.send(query)
    # print("Sent")
    # print("Receiving...")
    result =  ws.recv()
    # print("Received '%s'" % result)
    ws.close()
    return result

# query = '{"jsonrpc":"2.0","method":"eth_getBlockByHash","params": ["0xdd160e470118c3228a63495fe2990055938907b60fd6133a7c72be8c8f0fca61",false],"id":1}'
# url = 'wss://ropsten.infura.io/ws/4a6762bdc2e34b08b84a3b14f337093b'
# url = 'wss://mainnet.infura.io/ws/4a6762bdc2e34b08b84a3b14f337093b'
# query = '{"jsonrpc":"2.0","method":"eth_getBlockByHash","params": ["0x47d33942e7aaf4ce8da8d0e12ac1561be5dff5310c24110f2a919a128c1a6830",false],"id":1}'
# get_transactions_from_block(url,query)