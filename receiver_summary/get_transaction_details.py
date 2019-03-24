import requests
from websocket import create_connection
import json

def get_ws_connection(url):
    ws = create_connection(url)
    return ws

def get_transaction_details(ws, query):
    # ws = create_connection(url)
    ws.send(query)
    result =  ws.recv()
    # ws.close()
    return result

def get_gas_price(result):
    result = json.loads(result)
    try:
        result = result['result']
        gas_price = result["gasPrice"]
        gas_price = int(gas_price,16)/1000000000
        return gas_price
    except Exception as e:
        print(e)
        return None

def get_gas_used(result):
    result = json.loads(result)
    try:
        result = result['result']
        gas_used = result['gasUsed']
        gas_used = int(gas_used,16)
        return gas_used
    except Exception as e:
        print(e)
        return None

def get_gas(result):
    result = json.loads(result)
    try:
        result = result['result']
        gas = result['gas']
        gas = int(gas,16)
        return gas
    except Exception as e:
        print(e)
        return None