from flask import jsonify
import requests
import json
from requests.auth import HTTPBasicAuth
import get_url

# RPC 2.0 Headers -- Coindaddy
url = "http://public.coindaddy.io:4000/api/"
headers = {"content-type": "application/json"}
auth = HTTPBasicAuth("rpc", "1234")

# # RPC 2.0 Headers -- Counterparty
# url = "http://public.counterparty.io:4000/api/"
# headers = {"content-type": "application/json"}
# auth = HTTPBasicAuth("rpc", "rpc")

# Get asset info for longname
def get_name(asset_name):
    payload = {
        "method": "get_asset_info",
        "params": {
            "assets": [asset_name]
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=20)

    data = response.json()

    if(len(data["result"]) > 0):
        return data["result"][0]
    else:
        print("NO OWNER")
        return False

# Check account for asset
def confirm_asset(name, address, dev_mode=False):
    if(dev_mode):
        name = "TESTGEN." + name
    else:
        name = "QUESTFREN." + name
    # Gets A name from asset name
    try:
        # XCP node poll
        asset = get_name(name)
    except requests.exceptions.Timeout:
        # Xchain fallback
        print("Querying xchain...")
        print("https://xchain.io/api/asset/" + str(name))
        xchain_url = "https://xchain.io/api/asset/" + str(name)
        response = requests.get(xchain_url, json={"key": "value"})
        print(response.json())
        asset = response.json()

    # If no owner found end func
    if(asset == False):
        return False

    print("Querying address for asset")
    payload = {
        "method": "get_balances",
        "params": {
            "filters": [
                {"field": "address", "op": "==", "value": address},
                {"field": "quantity", "op": ">", "value": "0"},
            ],
            "filterop": "AND",
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=20)

    data = response.json()

    # Search for asset in address balance
    print(["asset"])
    for entry in data["result"]:
        if entry["asset"] == asset["asset"]:
            print(name + " FOUND")
            return [asset["asset"], address]

    return False

# Gets broadcasts
def mint_signature(address, fren_number, dev_mode=False):

    payload = {
        "method": "get_broadcasts",
        "params": {
            "filters": 
            [
                {"field": "block_index", "op": ">", "value": 727000},
                {"field": "source", "op": "==", "value": str(address)},
            ],
            "filterop": "AND",
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=20)

    data = response.json()

    # Parse log for messages signed by input address
    log = []
    for message in data["result"]:
        if message["source"] == address:
            log.append(message)

    
    # Reverse log to find first broadcast message
    # log.reverse()
    print(log)

    ## TODO:
    # Ensure getting the most recent mint signature, or first??
    # log.reverse()

    # Check log for mint messages
    for message in log:
        # Split message
        split_message = message["text"].upper().split()
        print(split_message)
        
        # If message fits template: "mint questfren n" then return true
        ########## NOOOOOTEEEEEEE: change message [1] to QUESTFREN after debug
        asset_prefix = "QUESTFREN"
        if(dev_mode):
            asset_prefix = "TESTGEN"

        if split_message[0] == "MINT" and split_message[1] == asset_prefix and str(split_message[2]) == str(fren_number):
            # print(message)
            return message
    
    # If not found return false
    return False

# Gets asset info for qf
def asset_info(i):
    print("I: " + str(i))
    url = "http://public.coindaddy.io:4000/api/"
    headers = {'content-type': 'application/json'}
    auth = HTTPBasicAuth('rpc', "1234")

    payload = {
        "method": "get_assets",
        "params": {
            "filters": 
                [
                    # {"field": "asset_name", "op": "==", "value": "QUESTFREN" },
                    {"field": "asset_longname", "op": "==", "value": "QUESTFREN." + str(i) },
                    {"field": "block_index", "op": ">", "value": 726000 }
                ],
                "filterop": "AND"
            # "asset": asset
            # "assets": ["QUESTFREN"]
        },
        "jsonrpc": "2.0",
        "id": 0
    }

    print(payload)

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    data = response.json()
    print(data)
    return data["result"]

    # # res = get_url.json("https://xchain.io/api/asset/QUESTFREN")
    # return data

def get_dispensers(list):
    url = "http://public.coindaddy.io:4000/api/"
    headers = {'content-type': 'application/json'}
    auth = HTTPBasicAuth('rpc', "1234")

    # print("LIST")
    # print(list[3])

    payload = {
        "method": "get_dispensers",
        "params": {
            "filters": 
                list,
            "filterop": "OR"
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    # print("PAYLOAD")
    # print(payload)

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    data = response.json()

    print(data)
    return data