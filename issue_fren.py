import requests
import json
from requests.auth import HTTPBasicAuth

# RPC 2.0 Headers -- Coindaddy
url = "http://public.coindaddy.io:4000/api/"
headers = {"content-type": "application/json"}
auth = HTTPBasicAuth("rpc", "1234")

def issue_fren(number):
    source = "1EWFR9dMzM2JtrXeqwVCY1LW6KMZ1iRhJ5"
    asset = "QUESTFRENS." + number
    quant = 1
    divisible = False
    description = "https://frenzone.net/questfrens/data/" + number + ".json"

    # Create_issuance xcp transaction
    payload = {
        "method": "create_issuance",
        "params": [
            {"source": source},
            {"asset": asset},
            {"quantity": quant},
            {"divisible": divisible},
            {"description": description}
        ],
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=20)

    print(response)