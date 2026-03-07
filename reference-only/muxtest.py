import json
import re
import muxgen

print("Loading world...")

world = open("world.json", "r")
jason = json.load(world)

def get_name(ent):
    if(ent.get("Components") == None or ent["Components"].get("NamedEntity") == None):
        return ""
        
    return ent["Components"]["NamedEntity"]["EntityName"]

regex = r"m1i_([0-9])"
def find_inputs():
    ret = {}
    
    # item for item in iterable if condition(item)
    for ent in jason["Entities"]:
        match = re.search(regex, get_name(ent))
        if (match != None):
            ret[int(match.group(1))]=ent
    
    return ret
    
    

def is_relay(ent):
    return ent["Template"] == "Relay.Folktails"

def get_coords(ent):
    x = ent["Components"]["BlockObject"]["Coordinates"]["X"]
    y = ent["Components"]["BlockObject"]["Coordinates"]["Y"]
    
    return (x,y)

inputs = find_inputs()
zero_loc = get_coords(inputs[0])
one_loc = get_coords(inputs[1])

mux = muxgen.muxgen((79, 255, 4), (0, -1), (1, 0), 8, "mux", inputs)
muxgen.print_mux(mux)

# def muxgen(start, wideways, deepways, bits, prefix, inputs):

for ident in mux["inv_ins"]:
    jason["Entities"].append(mux["inv_ins"][ident])
    
for ident in mux["internal"]:
    jason["Entities"].append(mux["internal"][ident])
    
for ident in mux["output"]:
    jason["Entities"].append(mux["output"][ident])

print("Writing output world")

out = open("out-muxtest-world.json", "w")
json.dump(jason, out)