# A little world-file consistency checker, for people programatically editing Timberborn save files
# Currently runs two checks:
# - Check to see that relays and memories all refer to existing entities, instead of pointing into the void
# - Check to make sure we don't have entities trying to occupy the same square.

# Check for internal consistency in a world json file - do all referenced IDs exist?

import json
import re
import sys

patchworld = open(sys.argv[1], "r")
patch_son = json.load(patchworld)

print("Checking entity references!")

def get_name(ent):
    return ent["Components"]["NamedEntity"]["EntityName"]

def is_relay(ent):
    return ent["Template"] == "Relay.Folktails"

def get_relays(raw):
    rels = filter(is_relay, raw["Entities"])
    relays = {}
    for rel in rels:
        relays[get_name(rel)] = rel
     
    return relays

def is_mem(ent):
    return ent["Template"] == "Memory.Folktails"
    
def get_mems(raw):
    mems = filter(is_mem, raw["Entities"])
    memories = {}
    for mem in mems:
        memories[get_name(mem)] = mem
     
    return memories
    
def is_lever(ent):
    return ent["Template"] == "Lever.Folktails"
    
def get_levers(raw):
    levs = filter(is_lever, raw["Entities"])
    levers = {}
    for lev in levs:
        levers[get_name(lev)] = lev
     
    return levers
    
def is_timer(ent):
    return ent["Template"] == "Timer.Folktails"
    
def get_timers(raw):
    tims = filter(is_timer, raw["Entities"])
    timers = {}
    for tim in tims:
        timers[get_name(tim)] = tim
     
    return timers
    
relays = get_relays(patch_son)
memories = get_mems(patch_son)
levers = get_levers(patch_son)
timers = get_timers(patch_son)

# build a set of known entities

known_ents = set()

for rel_key in relays:
    relay = relays[rel_key]
    
    known_ents.add(relay["Id"])

for mem_key in memories:
    memory = memories[mem_key]
    
    known_ents.add(memory["Id"])
    
for lev_key in levers:
    lever = levers[lev_key]
    
    known_ents.add(lever["Id"])
    
for tim_key in timers:
    timer = timers[tim_key]
    
    known_ents.add(timer["Id"])

# And now make sure every entity we reference is known

fails = 0

for rel_key in relays:
    relay = relays[rel_key]
    
    a = relay["Components"]["Relay"].get("InputA")
    b = relay["Components"]["Relay"].get("InputB")
    
    if(a != None):
        if (not a in known_ents):
            print("Entity A not found from referrant: " + str(relay))
            fails += 1
            
    if(b != None):
        if (not b in known_ents):
            print("Entity B not found from referrant: " + str(relay))
            fails += 1

for mem_key in memories:
    memory = memories[mem_key]
    
    a = memory["Components"]["Memory"].get("InputA")
    b = memory["Components"]["Memory"].get("InputB")
    
    if(a != None):
        if (not a in known_ents):
            print("Entity A not found from referrant: " + str(memory))
            fails += 1
            
    if(b != None):
        if (not b in known_ents):
            print("Entity B not found from referrant: " + str(memory))
            fails += 1

if (fails == 0):
    print("All references check out!")
    
print("Checking relay locations for collisions...")

ent_locs = {}

fails = 0

for ent in patch_son["Entities"]:
    if (ent["Components"].get("BlockObject") != None):
        coordinates = ent["Components"]["BlockObject"]["Coordinates"]
        xyz = (coordinates["X"], coordinates["Y"], coordinates["Z"])
        
        collide = ent_locs.get(xyz)
        
        if(collide != None):
            print("Entity collision at " + str(xyz) + " ! IDs: " + ent["Id"] + ", " + collide["Id"] + ": " + get_name(ent) + " & " + get_name(collide))
            fails += 1
        else:
            ent_locs[xyz] = ent
        
if (fails == 0):
    print("No entity collisions")