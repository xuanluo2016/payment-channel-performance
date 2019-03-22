import requests
from websocket import create_connection

def get_transactions_details(url, query):
    ws = create_connection(url)
    ws.send(query)
    result =  ws.recv()
    ws.close()
    return result

