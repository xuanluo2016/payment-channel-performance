from websocket import create_connection

def get_transactions_from_block(query):
    ws = create_connection("wss://mainnet.infura.io/ws/4a6762bdc2e34b08b84a3b14f337093b")
    print("Sending 'Hello, World'...")
    print(query)
    ws.send(query)
    print("Sent")
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)
    ws.close()
    return result

# query = '{"jsonrpc":"2.0","method":"eth_getBlockByHash","params": ["0x017576d599653160246e5eea1ebfa4e6db38260343c3d65ab685715d6ccc3a13",false],"id":1}'
# get_transactions_from_block(query)