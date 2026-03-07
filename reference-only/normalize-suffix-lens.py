import json
import re

testworld = open("world-testing.json", "r")

test_son = json.load(testworld)

print("world-testing data loaded")

print(str(len(test_son["Entities"])) + " entities found")

def is_relay(ent):
    return ent["Template"] == "Relay.Folktails"

pattern = r"(([a-zA-Z]*_)*([0-9]*_)?)([0-9]+)"

test_relays = list(filter(is_relay, test_son["Entities"]))

for rel in test_relays:
    name = rel["Components"]["NamedEntity"]["EntityName"]
    match = re.search(pattern, name)
    
    if(match):
        pref = match.group(1)
        suf = int(match.group(4))
        if(suf < 10):
            rel["Components"]["NamedEntity"]["EntityName"] = (pref + format(suf, '02d'))
    
print("\n" + str(len(test_relays)) + " relays found \n")

def is_mem(ent):
    return ent["Template"] == "Memory.Folktails"

test_mems = list(filter(is_mem, test_son["Entities"]))

for mem in test_mems:
    name = mem["Components"]["NamedEntity"]["EntityName"]
    match = re.search(pattern, name)
    
    if(match):
        pref = match.group(1)
        suf = int(match.group(4))
        if(suf < 10):
            mem["Components"]["NamedEntity"]["EntityName"] = (pref + format(suf, '02d'))


print("\n" + str(len(test_mems)) + " memory cells found\n")

print("writing output")

outputworld = open("output-world.json", "w")

json.dump(test_son, outputworld)

print("done")