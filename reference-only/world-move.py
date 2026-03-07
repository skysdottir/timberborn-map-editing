import json
import re
import muxgen

# Gotta move...
# Adder: add_*
# notter: not_N
# Switch: swa_*, swo_*, sws_*
# ANDer: and_*
# XORer: xor_*

print("Loading world...")

world = open("world.json", "r")
jason = json.load(world)

def get_name(ent):
    if(ent.get("Components") == None or ent["Components"].get("NamedEntity") == None):
        return ""
        
    return ent["Components"]["NamedEntity"]["EntityName"]

def find_by_name(regex):
    # item for item in iterable if condition(item)
    for ent in jason["Entities"]:
        match = re.search(regex, get_name(ent))
        if (match != None):
            yield ent
    
    

def is_relay(ent):
    return ent["Template"] == "Relay.Folktails"

pattern = r"(([a-zA-Z]+_)([a-zA-Z0-9]*_)*)([0-9]+)"

def get_coords(ent):
    x = ent["Components"]["BlockObject"]["Coordinates"]["X"]
    y = ent["Components"]["BlockObject"]["Coordinates"]["Y"]
    
    return (x,y)

relays = find_by_name(r"^(add|not|sw[aos]?|and|xor)_.*")

for relay in relays:
    orig_coords = get_coords(relay)
    orig_x = orig_coords[0]
    name = get_name(relay)
    
    new_coords = (orig_coords[0]+16, orig_coords[1])
    
    relay["Components"]["BlockObject"]["Coordinates"]["X"] = new_coords[0]
    
    print(name +" : " + str(orig_coords) + " -> " + str(new_coords))

 
print("Writing world out...")
 
out = open("out-world-shifted.json", "w")
json.dump(jason, out)
