from doctest import master
import requests
import json
from requests.auth import HTTPBasicAuth
from collections import Counter
from hashlib import sha256
from random import randrange


import get_url

# # Gets random int
# def get_random(floor, ceil, count):
#     # Get random number from API
#     url = "http://www.randomnumberapi.com/api/v1.0/random?min=" + str(floor) + "&max=" + str(ceil) + "&count=" + str(count)
#     res = get_url.json(url)
#     print(json.dumps(res))
#     return res

# Converts tx_id into Sha256 and then into ints
def generate_attr(tx_id):

    # Hash tx_id
    hashed_tx = sha256(tx_id.encode('utf-8')).hexdigest()
    # print("HASHED")
    # print(hashed_tx)

    # Split hex string into hexadecimal numbers
    n = 2
    seed_row = [(str(hashed_tx)[i:i+n]) for i in range(0, len(str(hashed_tx)), n)]
    # print(seed_row)

    # Convert to int
    int_list = []
    for entry in seed_row:
        to_int = int(entry, 16)
        int_list.append(to_int)

    # print("Seed attributes: ")
    # print(int_list)

    return int_list

masterlist = []

for i in range(1,255):
    
    tx_id = "a94b9a4574b4a01519e93a3acefaa74eab9474605cec22e1820d8f0ff5ee8246" + str(i)

    masterlist =  generate_attr(tx_id)

    random_num = randrange(255)
    # print(masterlist[10])
    if masterlist[10] == int(random_num):
        print("JACKPOT")

# # RPC 2.0 Headers -- Coindaddy
# url = "http://public.coindaddy.io:4000/api/"
# headers = {"content-type": "application/json"}
# auth = HTTPBasicAuth("rpc", "1234")


# payload = {
#     "method": "get_broadcasts",
#     "params": {
#         "filters": 
#             {"field": "block_index", "op": ">", "value": 600000},
#     },
#     "jsonrpc": "2.0",
#     "id": 0,
# }
# response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=20)

# data = response.json()

# # print(data["result"][0])

# masterlist = []

# for broadcast in data["result"]:

#     hashed_tx = sha256(broadcast["tx_hash"].encode('utf-8')).hexdigest()
#     # print(hashed_tx)

#     # Split hex string into hexadecimal numbers
#     n = 2
#     seed_row = [(str(hashed_tx)[i:i+n]) for i in range(0, len(str(hashed_tx)), n)]

#     # print(seed_row)

#     # Convert hex numbers to integers
#     for number in seed_row:
#         # print(number)
        
#         hex_num = int(number, 16)
#         masterlist.append(hex_num)
    
#     # print(seed_row)

#     # masterlist = seed_row + masterlist
#     # print(str(seeds))

# Count masterlist
# print(masterlist[10])
c = Counter(masterlist)
# print(c)
