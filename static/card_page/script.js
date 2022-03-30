// Gets fren details

const urlParams = new URLSearchParams(window.location.search);
const fren = urlParams.get('fren');
console.log(fren)

// Get fren JSON

const url = "https://frenzone.net/questfrens/data/" + fren + ".json"

function loadJSON(callback) {   
    let xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', '../news_data.json', true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            callback(JSON.parse(xobj.responseText));
        }
    };
    xobj.send(null);  
}

const getFrenData = async () => {
    const response = await fetch(url);
    const frenData = await response.json();
    console.log(frenData)

    const clothes = await fetch("https://frenzone.net/questfrens/card/items/clothes.json");
    const clothesData = await clothes.json();

    const head = await fetch("https://frenzone.net/questfrens/card/items/head.json");
    const headData = await head.json();
    // console.log(frenData.image_large)

    // Update image
    // TODO: Add placeholder
    document.getElementById('image').src = frenData.image_large

    // Update name
    if(frenData.alias != "") {
        document.getElementById('name').innerHTML = frenData.alias
    } else {
        document.getElementById('name').innerHTML = "QUESTFREN " + frenData.name
    }

    // Set stats
    let hitpoints = frenData.HP

    let healing_floor = 0
    let off_healing_floor = 0
    let uniq_healing_floor = 0
    let healing_ceil = 0
    let off_healing_ceil = 0
    let uniq_healing_ceil = 0

    let attack_floor = 0
    let off_attack_floor = 0
    let uniq_attack_floor = 0
    let attack_ceil = 0
    let off_attack_ceil = 0
    let uniq_attack_ceil = 0

    let defence = 0
    let strength = frenData.STR
    let constitution = frenData.CONST
    let dexterity = frenData.DEX
    let wisdom = frenData.WIS
    let intelligence = frenData.INTEL
    let charisma = frenData.CHAR

    // Inventory
    let inventory = {
        "clothes": "",
        "head": "",
        "main_hand": "",
        "off_hand": ""
    }

    // Update Items
    // Check for unique
    slot = ""   // Fill slot to skip relevant regular item
    if(frenData.unique !== 0) {
        console.log("Unique found!")

        const uniqueRes = await fetch("https://frenzone.net/questfrens/card/items/unique.json");
        const uniqueData = await uniqueRes.json();

        console.log(uniqueData)

        for(item of uniqueData) {
            if(item.number == frenData.unique) {
                console.log(item)

                // Get item slot
                slot = item.slot
                console.log("Slot: " + slot)

                // Add item to inventory
                if(slot == "clothes") {
                    inventory.clothes = item.name
                } else if (slot == "head") {
                    inventory.head = item.name
                } else if (slot == "main") {
                    console.log("to main")
                    inventory.main_hand = item.name
                } else if (slot == "off") {
                    inventory.off_hand = item.name
                }

                // Add item stats to card
                uniq_attack_floor = uniq_attack_floor + item.damage_floor
                uniq_attack_ceil = uniq_attack_ceil + item.damage_ceil

                uniq_healing_floor = item.healing_floor
                uniq_healing_ceil = item.healing_ceil

                hitpoints = hitpoints + item.HP
                strength = strength + item.STR
                dexterity = dexterity + item.DEX
                intelligence = intelligence + item.INTEL
                wisdom = wisdom + item.WIS

                // Add modifiers
                if(item.multiplier !== "") {
                    
                    // If multi is for damage
                    if(item.multiplier == "STR") {
                        console.log("Fren strength: " + strength)
                        console.log("pre: " + uniq_attack_floor + "-" + uniq_attack_ceil)
                        uniq_attack_floor = Math.floor((uniq_attack_floor * strength) / 10)
                        uniq_attack_ceil = Math.ceil((uniq_attack_ceil * strength) / 10)
                        console.log("post: " + uniq_attack_floor + "-" + uniq_attack_ceil)
                    } else if (item.multiplier == "DEX") {
                        uniq_attack_floor = Math.floor((uniq_attack_floor * dexterity) / 10)
                        uniq_attack_ceil = Math.ceil((uniq_attack_ceil * dexterity) / 10)
                    }
                    // If multi is wisdom
                    else if (item.multiplier == "WIS") {
                        uniq_healing_floor = uniq_healing_floor + Math.floor(wisdom / 2)
                        uniq_healing_ceil = uniq_healing_ceil + Math.ceil(wisdom / 2)
                    }
                    // If modifier is INT
                    else if (item.multiplier == "INTEL") {
                        console.log("Int multi")
                        uniq_attack_floor = uniq_attack_floor + Math.floor(intelligence / 2)
                        uniq_attack_ceil = uniq_attack_ceil + Math.ceil(intelligence / 2)
                    }

                }

                console.log("uniq atk")
                console.log(uniq_attack_floor + "-" + uniq_attack_ceil)
            }
        }
    }

    // Get clothes
    if(slot != "clothes") {
        for(item of clothesData) {
            
            if(frenData.clothes >= item.number_floor && frenData.clothes <= item.number_ceil ) {

                // Add item to inventory
                inventory.clothes = item.name
                
                defence = defence + item.defence
                hitpoints = hitpoints + item.HP
                strength = strength + item.STR
                dexterity = dexterity + item.DEX
                intelligence = intelligence + item.INTEL
                wisdom = wisdom + item.WIS
            }
        }
    }

    // Get head attributes
    if(slot != "head") {
        for(item of headData) {

            if(frenData.head >= item.number_floor && frenData.head <= item.number_ceil ) {

                // Add item to inventory
                inventory.head = item.name

                // console.log(item.name)

                defence = defence + item.defence
                hitpoints = hitpoints + item.HP
                strength = strength + item.STR
                dexterity = dexterity + item.DEX
                intelligence = intelligence + item.INTEL
                wisdom = wisdom + item.WIS
            }
        }
    }


    // Get head attributes
    if(slot != "main") {
        // Update weapons
        const mainHand = await fetch("https://frenzone.net/questfrens/card/items/main_hand.json");
        const mainHandData = await mainHand.json();
        
        for(item of mainHandData) {

            if(frenData.main_hand >= item.number_floor && frenData.main_hand <= item.number_ceil ) {
                // console.log(item)

                // Add item to inventory
                inventory.main_hand = item.name

                // Add item stats to card
                attack_floor = attack_floor + item.damage_floor
                attack_ceil = attack_ceil + item.damage_ceil
                console.log(attack_floor + "-" + attack_ceil)

                healing_floor = healing_floor + item.healing_floor
                healing_ceil = healing_ceil + item.healing_ceil

                hitpoints = hitpoints + item.HP
                strength = strength + item.STR
                dexterity = dexterity + item.DEX
                intelligence = intelligence + item.INTEL
                wisdom = wisdom + item.WIS

                // Add modifiers
                if(item.multiplier !== "") {
                    
                    // If multi is for damage
                    if(item.multiplier == "STR") {
                        // console.log("pre: " + attack_floor + "-" + attack_ceil)
                        attack_floor = Math.floor((attack_floor * strength) / 10)
                        attack_ceil = Math.ceil((attack_ceil * strength) / 10)
                        // console.log("post: " + attack_floor + "-" + attack_ceil)
                    } else if (item.multiplier == "DEX") {
                        // console.log("pre: " + attack_floor + "-" + attack_ceil)
                        attack_floor = Math.floor((attack_floor * dexterity) / 10)
                        attack_ceil = Math.ceil((attack_ceil * dexterity) / 10)
                        // console.log("post: " + attack_floor + "-" + attack_ceil)
                    }
                    // If multi is wisdom
                    else if(item.multiplier == "WIS") {
                        healing_floor = healing_floor + Math.floor(wisdom / 2)
                        healing_ceil = healing_ceil + Math.ceil(wisdom / 2)
                    }
                    // If modifier is INT
                    else if (item.multiplier == "INTEL") {
                        console.log("Int multi")
                        attack_floor = attack_floor + Math.floor(intelligence / 2)
                        attack_ceil = attack_ceil + Math.ceil(intelligence / 2)
                    }
                }
                
            }
        }
    }

    if(slot != "off") {
        const offHand = await fetch("https://frenzone.net/questfrens/card/items/off_hand.json");
        const offHandData = await offHand.json();
        // console.log(offHandData)

        // Get head attributes
        for(item of offHandData) {

            if(frenData.off_hand >= item.number_floor && frenData.off_hand <= item.number_ceil ) {
                // console.log("Off hand")
                // console.log(item)

                // Add item to inventory
                inventory.off_hand = item.name

                // Add item stats to card
                off_attack_floor = item.damage_floor
                off_attack_ceil = item.damage_ceil

                off_healing_floor = item.healing_floor
                off_healing_ceil = item.healing_ceil

                hitpoints = hitpoints + item.HP
                strength = strength + item.STR
                dexterity = dexterity + item.DEX
                intelligence = intelligence + item.INTEL
                wisdom = wisdom + item.WIS

                // Add modifiers
                if(item.multiplier !== "") {

                    // If multi is for damage
                    if(item.multiplier == "STR") {
                        off_attack_floor = Math.floor((off_attack_floor * strength) / 10)
                        off_attack_ceil = Math.ceil((off_attack_ceil * strength) / 10)
                    } else if (item.multiplier == "DEX") {
                        off_attack_floor = Math.floor((off_attack_floor * dexterity) / 10)
                        off_attack_ceil = Math.ceil((off_attack_ceil * dexterity) / 10)
                    }

                    // If multi is wisdom
                    else if(item.multiplier == "WIS") {
                        off_healing_floor = off_healing_floor + Math.floor(wisdom / 2)
                        off_healing_ceil = off_healing_ceil + Math.ceil(wisdom / 2)
                    }
                    // If multi is INT
                    else if (item.multiplier == "INTEL") {
                        off_attack_floor = off_attack_floor + Math.floor(intelligence / 2)
                        off_attack_ceil = off_attack_ceil + Math.ceil(intelligence / 2)
                    }
                }
            }
        }
    }

    // Update ATK
    if(attack_ceil > 0 || uniq_attack_ceil > 0 || off_attack_ceil > 0) {
        document.getElementById('attack').innerHTML = (off_attack_floor + attack_floor + uniq_attack_floor) + "-" + (off_attack_ceil + attack_ceil + uniq_attack_ceil)
    } else {
        document.getElementById('attack').innerHTML = 0
    }

    // Update Healing
    if(healing_ceil > 0 || uniq_healing_ceil > 0 || off_healing_ceil) {
        document.getElementById('healing').innerHTML = (off_healing_floor + healing_floor + uniq_healing_floor) + "-" + (off_healing_ceil + healing_ceil + uniq_healing_ceil)
    } else {
        document.getElementById('healing').innerHTML = 0
    }

    // Update DEF
    document.getElementById('defence').innerHTML = defence
    
    // Update HP
    document.getElementById('hp').innerHTML = hitpoints
    // If HP is low set HP colour to red
    if(hitpoints < 10) {
        document.getElementById('hp').style.color = "red"
    }

    // Update STR
    document.getElementById('strength').innerHTML = strength

    // Update CON
    document.getElementById('const').innerHTML = constitution

    // Update DEX
    document.getElementById('dex').innerHTML = dexterity

    // Update WIS
    document.getElementById('wis').innerHTML = wisdom

    // Update INT
    document.getElementById('int').innerHTML = intelligence

    // Update CHAR
    document.getElementById('char').innerHTML = charisma

    // Update inventory
    console.log(inventory)

    document.getElementById("clothes").innerHTML = inventory.clothes
    document.getElementById("head").innerHTML = inventory.head
    document.getElementById("main").innerHTML = inventory.main_hand
    document.getElementById("off").innerHTML = inventory.off_hand

    document.getElementById("inventory").innerHTML = inventoryDOM
};

getFrenData();