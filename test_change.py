import get_url
import json
import upload_to

res = get_url.json("https://frenzone.net/questfrens/items/unique.json")

for item in res:
    print(item)
    if item['number'] == 1:
        item['minted'] = True

print(res)

upload_to.s3("unique", json.dumps(res, indent=4, ensure_ascii=False), ".json", "items/")