from xml.etree.ElementPath import find
from flask import Flask, jsonify
from flask import request
from flask import jsonify
import json
import time
import os
import boto3
from flask_cors import cross_origin, CORS

import query_xcp
import generate
import upload_to
import get_url

app = Flask(__name__)

# add CORS
CORS(app)

## REMINDER ##
# Change asset check from TESTGEN to QUESTFREN when live

## TODO:
# Log purchases?

@cross_origin()
@app.route("/")
def home():
    return "Index"

@app.route("/mint")
def mint():
    ## Dev mode
    # Changes QUESTFRENS asset to TESTGEN
    dev_mode = False
    ## TODO:
    # DYNAMICALLY GENERATE MINT JSON

    # Get NFT name
    fren_number = str(request.args.get('fren'))
    address = str(request.args.get('address'))

    if int(fren_number) < 0 or int(fren_number) > 10000:
        return jsonify({"error": "Fren number out of bounds"})

    # Check that input is numeric only
    if(fren_number.isnumeric()):
        # Mint check checks:
        #   1. Asset is held by address
        #   2. Asset has not already been minted
        asset_info = query_xcp.confirm_asset(fren_number, address, dev_mode)    # Dev mode is True
        # print(asset_info)

        # Check asset has not already been minted
        json_url = "https://frenzone.net/questfrens/data/" + str(fren_number) + ".json"
        fren_json = get_url.json(str(json_url))
        # print("FRENJSON")
        # print(fren_json)
        
        # Cancels mint operation if already minted, unless dev mode is true
        if(fren_json == False):
            return jsonify({"error": "Fren JSON not found"})
        
        if(fren_json["minted"] == True and dev_mode == False):
            asset_info = False  # Invalidate mint check if already minted
            return jsonify({"error": "Fren already minted"})

        # Search broadcasts for mint signature
        if(asset_info):

            # Check if address has signed a mint message
            signature = query_xcp.mint_signature(asset_info[1], fren_number, dev_mode)

            # If mint has been signed then generate asset
            if signature:
                # Get seed from tx hash
                seed = signature["tx_hash"]

                # Run image generation
                attr = generate.fren(fren_number, seed)

                # Open template json
                path = "./static/fren/template.json"
                # print("open: " + path)
                with open(path) as f:
                    json_data = json.load(f)
                    # print(json_data)

                ## TODO:
                #  1. Generate database entry of minted fren
                #  2. Also append to backup masterlist on S3

                # Update JSON
                # Alias
                find_alias = signature["text"].split()
                if(len(find_alias) > 3):
                    print("ALIAS: " + find_alias[3])
                    
                    # Set alias
                    json_data["alias"] = find_alias[3] # CHECK THIS WORKS WITHOUT ALIAS

                    # Check alias is not profane
                    file = open("profane.txt")
                    if find_alias[3] in file.read():
                        print(find_alias[3])
                        find_alias[3] = ""
                        json_data["alias"] = ""

                    # Limit alias length
                    if len(find_alias[3]) > 15:
                        json_data["alias"] = ""

                    # If alias contains questfren remove
                    if "questfren" in find_alias[3].lower():
                        json_data["alias"] = ""

                    masterlist_json = get_url.json("https://frenzone.net/questfrens/masterlist/masterlist.json")

                    for asset in masterlist_json:
                        # print(asset["alias"] + "  -  " + find_alias[3])
                        if find_alias[3].lower() == asset["alias"].lower():
                            print("DUPLICATE NAME")
                            json_data["alias"] = ""

                else:
                    json_data["alias"] = ""

                json_data["name"] = fren_number
                json_data["minted"] = True
                json_data["seed"] = seed
                json_data["mint_address"] = asset_info[1]
                json_data["mint_time"] = time.time()
                json_data["image"] = "https://frenzone.net/questfrens/icons/" + fren_number + "-thumb.png"
                json_data["image_large"] = "https://frenzone.net/questfrens/images/" + fren_number + ".png"
                # Stats
                json_data.update({"HP": attr[0]})
                json_data.update({"STR": attr[1]})
                json_data.update({"CONST": attr[2]})
                json_data.update({"DEX": attr[3]})
                json_data.update({"INTEL": attr[4]})
                json_data.update({"WIS": attr[5]})
                json_data.update({"CHAR": attr[13]})
                # Items
                json_data.update({"body": attr[6]})
                json_data.update({"eyes": attr[7]})
                json_data.update({"clothes": attr[8]})
                json_data.update({"head": attr[9]})
                json_data.update({"main_hand": attr[10]})
                json_data.update({"off_hand": attr[11]})
                json_data.update({"unique": attr[12]})
                # Card iFrame
                # Create iframe escape json
                json_data.update({"website": "https://questfrens.io/"})
                iframe = ("<iframe style=\"border:0;\" width=\"400\" height=\"560\" src=\"https://frenzone.net/questfrens/card/index.html?fren=%s\"></iframe> \r\n\r\n<img hidden src=\"lkjasdkljasljkdas.jpg\" onerror=\"this.onerror = null;try{console.log('hello');document.querySelectorAll('#digitalArtInfo, #additionalCustomInfo ').forEach((elt)=>elt.setAttribute('hidden',true));document.querySelector('#assetExtendedDescription').classList.add('text-center');}catch(e){console.log(e)}\">" % fren_number)
                
                json_data.update({"description": iframe})

                # # Upload JSON to S3
                # Create object
                jsonified_obj = json.dumps(json_data, indent=4, ensure_ascii=False)

                # Create object name
                filename = str(fren_number)

                # Upload to s3
                upload_to.s3(filename, jsonified_obj, ".json", "data/")

                # Add to master questfren json on s3
                master_url = "https://frenzone.net/questfrens/masterlist/masterlist.json"
                master_json = get_url.json(str(master_url))
                print("master")
                print(master_json)

                master_json.append(json_data)
                jsonified_master = json.dumps(master_json, indent=4, ensure_ascii=False)

                # Upload master json
                upload_to.s3("masterlist", jsonified_master, ".json", "masterlist/")

                return jsonify(json_data)
            else:
                return jsonify({"error": "Signature not found."})

        else:
            return jsonify({"error": "Asset not found in address."})
    else:
        return jsonify({"error": "Incorrect asset parameters"})



# Gets dispensers
@app.route("/get_dispensers")
def get_dispensers():

    # Open name list
    name_file = get_url.json("https://frenzone.net/questfrens/masterlist/name_list.json")
    # with open('name_list.json') as name_file:
    #     name_data = json.load(name_file)
    #     # print(name_data)

    asset_list = []

    # Create list
    for asset in name_file:
        # print(asset)
        # {"field": "asset", "op": "LIKE", "value": "name" }
        asset_list.append({"field": "asset", "op": "==", "value": asset["asset_name"] })

    # print(asset_list)

    res = query_xcp.get_dispensers(asset_list)

    # Remove closed dispensers
    final_list = []

    for dispenser in res["result"]:
        if int(dispenser["give_remaining"]) > 0:
            final_list.append(dispenser)

    # with open('dispenser_list.json', 'w') as fp:
    #     json.dump(final_list, fp)


    return jsonify(final_list)


# Gets asset longnames
@app.route("/get_longnames")
def get_names():

    # # Open name list from s3
    name_file = get_url.json("https://frenzone.net/questfrens/masterlist/name_list.json")
    # name_data = json.load(name_file)

    # Get last read Questfren
    last_read = 0
    for asset in name_file:
        split_name = asset["asset_longname"].split(".")
        print(split_name)
        if int(split_name[1]) > last_read:
            last_read = int(split_name[1])
            print(last_read)

    running = True
    while running == True:
        res = query_xcp.asset_info(last_read + 1)

        # Append to masterlist
        try:
            name_file.append(res[0])
            last_read += 1
        except:
            running = False
            break

    # Upload new items to list on s3
    if len(name_file) > 0:
        jsonified_master = json.dumps(name_file, indent=4, ensure_ascii=False)
        upload_to.s3("name_list", jsonified_master, ".json", "masterlist/")

    return jsonify(name_file)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run("0.0.0.0", 8080)