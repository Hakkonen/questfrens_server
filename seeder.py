from doctest import master
import requests
import json
from requests.auth import HTTPBasicAuth
from collections import Counter
from hashlib import sha256

import get_url

# Gets random int
def get_random(floor, ceil, count):
    # Get random number from API
    url = "http://www.randomnumberapi.com/api/v1.0/random?min=" + str(floor) + "&max=" + str(ceil) + "&count=" + str(count)
    res = get_url.json(url)
    print(json.dumps(res))
    return res

# Converts tx_id into Sha256 and then into ints
def generate_attr(tx_id):

    # Hash tx_id
    hashed_tx = sha256(tx_id.encode('utf-8')).hexdigest()
    print("HASHED")
    print(hashed_tx)

    # Split hex string into hexadecimal numbers
    n = 2
    seed_row = [(str(hashed_tx)[i:i+n]) for i in range(0, len(str(hashed_tx)), n)]
    print(seed_row)

    # Convert to int
    int_list = []
    for entry in seed_row:
        to_int = int(entry, 16)
        int_list.append(to_int)

    print("Seed attributes: ")
    print(int_list)

    return int_list