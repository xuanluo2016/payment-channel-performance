from websocket import create_connection

get_transactions_from_block(query):
    ws = create_connection("wss://mainnet.infura.io/ws/4a6762bdc2e34b08b84a3b14f337093b")
    print("Sending 'Hello, World'...")
    ws.send(query)
    print("Sent")
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)
    ws.close()
    return result
