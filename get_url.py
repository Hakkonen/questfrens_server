from flask import request
from flask import jsonify
import requests

def json(url):
    res = requests.get(url)
    if(res.status_code == 200):
        return res.json()
    else:
        print(res.status_code)
        return False