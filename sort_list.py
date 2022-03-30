import json
import operator

with open('masterlist.json') as f:
    masterlist = json.load(f)

sorted_list = sorted(masterlist, key=lambda x: x["mint_time"])

jsonified_master = json.dumps(masterlist, indent=4, ensure_ascii=False)

with open('masterlist2.json', 'w') as fp:
    json.dump(jsonified_master, fp)