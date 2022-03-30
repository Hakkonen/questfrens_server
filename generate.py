from distutils.command.upload import upload
# from flask import request
from os import walk
from select import select
from PIL import Image
import upload_to
import io
from random import randrange
import math
import json

import seeder
import get_url

def get_attr(seed, attr):

    # Seed is int to find range of
    # Attr is the layer folder
    filenames = next(walk("./static/attributes/" + attr + "/"), (None, None, []))[2]
    # print("filenames")
    # print(filenames)

    # Find the image that has a name within the range of the seed
    for image in filenames:
        if image != ".DS_Store":
            image_split = image.split(".")       # Split name from filetype
            attr_range = image_split[0].split("-") # Split integers
            
            # Currently converting from hex
            if(seed >= int(attr_range[0]) and seed <= int(attr_range[1])):
                src = "./static/attributes/" + attr + "/" + image
                return src

def fren(fren_name, tx_id):
    
    # Get attributes from seed tx_id
    seed_attr = seeder.generate_attr(tx_id)

    ## TODO:
    # For each item have a 1 / 1000 chance of generating a unique item
    # Allow unique items only once, maybe call / update seperate JSON?

    ## Define attributes from seed
    # HP is raw seed INT
    hp = int(math.ceil((seed_attr[0] + 1) / 2))
    print("HP: " + str(hp))
    # STR is seed / 10
    strength = int(math.ceil(seed_attr[1] / 10))
    print("STR: " + str(strength))
    # CONST is HP / 10
    const = int(math.ceil(seed_attr[0] / 10))
    print("CONST: " + str(const))
    # DEX is seed / 10
    dex = int(math.ceil(seed_attr[2] / 10))
    print("DEX: " + str(dex))
    # INT is seed / 10
    intel = int(math.ceil(seed_attr[3] / 10))
    print("INT: " + str(intel))
    # WIS is seed / 10
    wis = int(math.ceil(seed_attr[4] / 10))
    print("WIS: " + str(wis))
    # CHA is seed / 10
    # Note seed is from 11th slot in array
    charisma = int(math.ceil(seed_attr[11] / 10))
    print("CHAR: " + str(charisma))

    ## Get item atrtibutes
    body = seed_attr[5]
    eyes = seed_attr[6]
    clothes = seed_attr[7]
    head = seed_attr[8]
    main_hand = seed_attr[9]
    off_hand = seed_attr[10]
    unique = 0

    # Determine if unique item or not
    # Unique item lists    
    unique_clothes = [ 2, 5, 12 ]
    unique_heads = [ 4, 7, 9 ]
    unique_mains = [ 1, 8, 10, 13 ]
    unique_offs = [ 3, 6, 11 ]

    # Unique item, set to 0 if null
    unique_item = 0

    unique_roll = seeder.get_random(1, 255, 1)[0]
    
    print("Lottery number: " + str(seed_attr[11]))
    print("Unique roll: " + str(unique_roll))

    if(seed_attr[11] == unique_roll): 
        print("Unique item won")
        # Randomly select unique item from list

        # Get remaining 
        unique_list = get_url.json("https://frenzone.net/questfrens/items/unique.json")
        # print(unique_list)

        tries = 0
        while tries < 30:
            # Increment attempt
            tries += 1

            # Generate random int
            rand_int = randrange(1, 14)

            for item in unique_list:
                # If this item number matches the random number cont.
                if int(item["number"]) == rand_int:
                    # If minted is false then select item
                    if(item["minted"] == False):
                        unique_item = rand_int

                        ## Modify remaining unique items
                        # Get list
                        unique_list = get_url.json("https://frenzone.net/questfrens/items/unique.json")
                        # print(unique_list)

                        # filter for item
                        for item in unique_list:
                            # If the item is the randomly selected item then set to minted
                            if item['number'] == rand_int:
                                item['minted'] = True

                                # Set attribute unique to item
                                unique = item["number"]

                                return_list = json.dumps(unique_list, indent=4, ensure_ascii=False)
                                # print(return_list)

                                # Reuplaod
                                upload_to.s3("unique", return_list, ".json", "items/")

                                tries = 31

    ## Collate relevant images into PNG
    # Open BG
    filenames = next(walk("./static/attributes/bg/"), (None, None, []))[2]
    # print(filenames)

    # Find the image that has a name within the range of the seed
    bg_src = "./static/attributes/bg/bg.png"
    # print(bg_src)
    bg = Image.open(bg_src)

    # Open body
    body_src = get_attr(body, "body")
    # print(body_src)
    body_img = Image.open(body_src)

    # Open eyes
    eyes_src = get_attr(eyes, "eyes")
    # print(eyes_src)
    eyes_img = Image.open(eyes_src)

    # Clothes
    if unique_item in unique_clothes:
        clothes_img = Image.open("./static/attributes/unique/" + str(unique_item) + ".png")
    else:
        clothes_src = get_attr(clothes, "clothes")
        # print(clothes_src)
        clothes_img = Image.open(clothes_src)

    # Open head
    if unique_item in unique_heads:
        head_img = Image.open("./static/attributes/unique/" + str(unique_item) + ".png")
    else:
        head_src = get_attr(head, "head")
        # print(head_src)
        head_img = Image.open(head_src)

    # Open main hand
    if unique_item in unique_mains:
        main_img = Image.open("./static/attributes/unique/" + str(unique_item) + ".png")
    else:
        main_src = get_attr(main_hand, "main")
        # print(main_src)
        main_img = Image.open(main_src)

    # Open off hand
    if unique_item in unique_offs:
        off_img = Image.open("./static/attributes/unique/" + str(unique_item) + ".png")
    else:
        off_src = get_attr(off_hand, "off")
        # print(off_src)
        off_img = Image.open(off_src)

    image_main = Image.new("RGBA", bg.size)
    image_main.paste(bg, (0,0), bg)
    image_main.paste(body_img, (0,0), body_img)
    image_main.paste(eyes_img, (0,0), eyes_img)
    image_main.paste(clothes_img, (0,0), clothes_img)
    image_main.paste(head_img, (0,0), head_img)
    image_main.paste(main_img, (0,0), main_img)
    image_main.paste(off_img, (0,0), off_img)

    # Save the image to an in-memory file
    in_mem_file = io.BytesIO()
    image_main.save(in_mem_file, format="PNG")
    in_mem_file.seek(0)

    # image_main.show()
    # image_main.save("./static/fren/" + str(fren_name) + ".png")

    ## Upload to s3
    # Image_large

    # Create object name
    image_name = str(fren_name)

    # Upload to s3
    upload_to.s3(image_name, in_mem_file, ".png", "images/")

    # Create thumbnail
    size = 48, 48
    thumb = image_main.resize(size, Image.ANTIALIAS)

    # Flush temp memory
    in_mem_file.seek(0)
    in_mem_file.truncate(0)

    # Save the thumb to an in-memory file
    in_mem_file = io.BytesIO()
    thumb.save(in_mem_file, format="PNG")
    in_mem_file.seek(0)

    # Upload thumbnail to S3
    thumb_name = str(fren_name) + "-thumb"
    upload_to.s3(thumb_name, in_mem_file, ".png", "icons/")

    # Save the image to an in-memory file
    in_mem_file = io.BytesIO()
    thumb.save(in_mem_file, format="PNG")
    in_mem_file.seek(0)

    # thumb.show()
    # thumb.save("./static/fren/" + str(fren_name) + "-thumb.png")

    # Flush temp memory
    in_mem_file.seek(0)
    in_mem_file.truncate(0)

    ## Thumbnail ###########
    # thumb = Image.new("RGBA", bg.size)
    # image_main.paste(body_img, (0,0), body_img)
    # image_main.paste(eyes_img, (0,0), eyes_img)
    # image_main.paste(clothes_img, (0,0), clothes_img)
    # image_main.paste(head_img, (0,0), head_img)
    # image_main.paste(main_img, (0,0), main_img)
    # image_main.paste(off_img, (0,0), off_img)

    # # Downsize
    # size = 48, 48
    # thumb.resize(size, Image.ANTIALIAS)

    # # Save the image to an in-memory file
    # in_mem_file = io.BytesIO()
    # thumb.save(in_mem_file, format="PNG")
    # in_mem_file.seek(0)

    # # Upload thumbnail to S3
    # thumb_name = str(fren_name) + "-thumb"
    # # upload_to.s3(thumb_name, in_mem_file, ".png", "icons/")

    # print("ATTRIBUTES")
    # print(attributes)

    # Flush temp memory
    in_mem_file.seek(0)
    in_mem_file.truncate(0)

    ## Return seed attributes
    attributes = [hp, strength, const, dex, intel, wis, body, eyes, clothes, head, main_hand, off_hand, unique, charisma]
    return attributes