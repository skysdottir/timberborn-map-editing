import json
import re
import uuid
import muxgen

# Okay - here's what we need to do.

# Find the existing mem, mema, and memo objects
# rename them to the new scheme (mem_, mem_r_, mem_x_)
# shift them to their new locations
# Generate new read, write, and exec muxes
# generate mem_x_a and mem_x_o for registers 13-31
# generate all new registers for 32-63
# wire Ms, As, and Os

# Zero point: (60, 255)

print("Loading world...")

world = open("world.json", "r")
jason = json.load(world)
entities = jason["Entities"]


def get_name(ent):
    if(ent.get("Components") == None or ent["Components"].get("NamedEntity") == None):
        return ""
        
    return ent["Components"]["NamedEntity"]["EntityName"]

def is_relay(ent):
    return ent["Template"] == "Relay.Folktails"

def is_memory(ent):
    return ent["Template"] == "Memory.Folktails"

def get_coords(ent):
    x = ent["Components"]["BlockObject"]["Coordinates"]["X"]
    y = ent["Components"]["BlockObject"]["Coordinates"]["Y"]
    
    return (x,y)

# Find the existing mem, mema, memo, and master bit objects

mem_pattern = r"mem_([0-9]+)_([0-9]+)"
memz_pattern = r"mem([ao])_([0-9]+)_([0-9]+)"
input_bit_pattern = r"^bit_([0-9]+)$"

mems = {}
mem_r_a = {}
mem_r_o = {}
input_bits = {}

all_other_entities = []

mem_count = 0
mema_count = 0
memo_count = 0
bit_count = 0

for entity in entities:
    if (is_memory(entity)):
        match = re.search(mem_pattern, get_name(entity))
        
        if(match != None):
            reg = int(match.group(1))
            bit = int(match.group(2))
            
            if(mems.get(reg) == None):
                mems[reg] = {}
            
            mems[reg][bit] = entity
            mem_count += 1
        else:
            all_other_entities.append(entity)

    elif (is_relay(entity)):
        match=re.search(memz_pattern, get_name(entity))
        bit_match = re.search(input_bit_pattern, get_name(entity))
        if(match != None):
            ao = match.group(1)
            reg = int(match.group(2))
            bit = int(match.group(3))
            
            wd = mem_r_a if ao == "a" else mem_r_o
            
            if(wd.get(reg) == None):
                wd[reg]={}
                
            wd[reg][bit] = entity
            
            if(ao == "a"):
                mema_count += 1
            else:
                memo_count += 1
        
        elif(bit_match != None):
            bit = int(bit_match.group(1))
            input_bits[bit]=entity
            bit_count += 1 # this had better end up at 16
        
        else:
            all_other_entities.append(entity)
    
    else:
        all_other_entities.append(entity)

print("Search done, found " + str(mem_count) + " memories, " + str(mema_count) + " anders, " + str(memo_count) + " or chains, and " + str(bit_count) + " bits")

# rename them to the new scheme (mem_, mem_r_, mem_x_)

for reg in mem_r_a:
    register = mem_r_a[reg]
    for bit in register:
        register[bit]["Components"]["NamedEntity"]["EntityName"] = "mem_r_a_" + str(reg) + "_" + str(bit)
        
for reg in mem_r_o:
    register = mem_r_o[reg]
    for bit in register:
        register[bit]["Components"]["NamedEntity"]["EntityName"] = "mem_r_o_" + str(reg) + "_" + str(bit)
        
# shift them to their new locations
# exec mux: 60-63
# read mux: 64-67
# Each memory cell is now 6 tall. +0: x_o. +1: x_a. +2: r_o. +3: r_a. +4: mem. +5: empty
# so, 68 + bit*6 (+ 2 bonus if bit>7)
# tops out at 166
# 168-172: write mux

def try_update(cells, register, bit, new_x):
    if(cells.get(register) == None):
        return
    
    if(cells[register].get(bit) == None):
        return
        
    cells[register][bit]["Components"]["BlockObject"]["Coordinates"]["X"] = new_x

for register in range(0, 32):
    for bit in range(0, 16):
        bonus = 0 if bit < 8 else 2
        new_base_x = 68 + bit*6 + bonus
        
        try_update(mems, register, bit, new_base_x + 4)
        try_update(mem_r_a, register, bit, new_base_x + 3)
        try_update(mem_r_o, register, bit, new_base_x + 2)

# Generate new read, write, and exec muxes
# from muxgen.py: muxgen(start, wideways, deepways, bits, prefix, inputs)
# specifying "None" input so they'll create input relays, I'll passthrough those to the relevant bits by hand

exec_mux = muxgen.muxgen((60,255,4), (0, -1), (1, 0), 6, "xd", None)
read_mux = muxgen.muxgen((64,255,4), (0, -1), (1, 0), 6, "rd", input_bits)
write_mux = muxgen.muxgen((172,255,4), (0, -1), (-1, 0), 6, "wd", None)

# generate mem_x_a and mem_x_o for registers 13-31. Not going to wire any of them yet, I'll have to do all that later.

# mem_x_a = {}
# mem_x_o = {}

# for register in range(13, 31):
    # mem_x_a[register] = {}
    # mem_x_o[register] = {}
    
    # for bit in range(0, 16):
        
        # regz = str(register)
        # bitz = str(bit)
        # bonus =  2 if (bit > 7) else 0
        
        # memxa = {"Id":str(uuid.uuid4()),"Template":"Relay.Folktails","Components":{"NamedEntity":{"EntityName":"mem_x_a_" + regz + "_" + bitz},"BlockObject":{"Coordinates":{"X":68+(6*bit)+1+bonus,"Y":255-register,"Z":4}},"Relay":{"Mode":"And"},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"Plank","Amount":1},{"Good":"Gear","Amount":1}]}}}}
        
        # memxo = {"Id":str(uuid.uuid4()),"Template":"Relay.Folktails","Components":{"NamedEntity":{"EntityName":"mem_x_o_" + regz + "_" + bitz},"BlockObject":{"Coordinates":{"X":68+(6*bit)+bonus,"Y":255-register,"Z":4}},"Relay":{"Mode":"Or"},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"Plank","Amount":1},{"Good":"Gear","Amount":1}]}}}}
        
        # mem_x_a[register][bit] = memxa
        # mem_x_o[register][bit] = memxo

# generate all new registers for 32-63
# for register in range(32, 63):
    # mem_x_a[register] = {}
    # mem_x_o[register] = {}
    # mem_r_a[register] = {}
    # mem_r_o[register] = {}
    # mems[register] = {}
    
    # for bit in range(0, 16):
        
        # regz = str(register)
        # bitz = str(bit)
        # bonus =  2 if (bit > 7) else 0
        
        # memxa_id = str(uuid.uuid4())
        # memxa = {"Id":str(uuid.uuid4()),"Template":"Relay.Folktails","Components":{"NamedEntity":{"EntityName":"mem_x_a_" + regz + "_" + bitz},"BlockObject":{"Coordinates":{"X":68+(6*bit)+1+bonus,"Y":255-register,"Z":4}},"Relay":{"Mode":"And"},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"Plank","Amount":1},{"Good":"Gear","Amount":1}]}}}}
        
        # memxo = {"Id":str(uuid.uuid4()),"Template":"Relay.Folktails","Components":{"NamedEntity":{"EntityName":"mem_x_o_" + regz + "_" + bitz},"BlockObject":{"Coordinates":{"X":68+(6*bit)+bonus,"Y":255-register,"Z":4}},"Relay":{"Mode":"Or"},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"Plank","Amount":1},{"Good":"Gear","Amount":1}]}}}}
        
        # mem_x_a[register][bit] = memxa
        # mem_x_o[register][bit] = memxo
        
        # memra_id = str(uuid.uuid4())
        # memra = {"Id":str(uuid.uuid4()),"Template":"Relay.Folktails","Components":{"NamedEntity":{"EntityName":"mem_r_a_" + regz + "_" + bitz},"BlockObject":{"Coordinates":{"X":68+(6*bit)+3+bonus,"Y":255-register,"Z":4}},"Relay":{"Mode":"And"},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"Plank","Amount":1},{"Good":"Gear","Amount":1}]}}}}
        
        # memro = {"Id":str(uuid.uuid4()),"Template":"Relay.Folktails","Components":{"NamedEntity":{"EntityName":"mem_r_o_" + regz + "_" + bitz},"BlockObject":{"Coordinates":{"X":68+(6*bit)+2+bonus,"Y":255-register,"Z":4}},"Relay":{"Mode":"Or"},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"Plank","Amount":1},{"Good":"Gear","Amount":1}]}}}}
        
        # mem_r_a[register][bit] = memra
        # mem_r_o[register][bit] = memro
        
        # mem = {"Id":str(uuid.uuid4()),"Template":"Memory.Folktails","Components":{"NamedEntity":{"EntityName":"mem_" + regz + "_" + bitz},"BlockObject":{"Coordinates":{"X":68+(6*bit)+4+bonus,"Y":255-register,"Z":4}},"Memory":{"Mode":"Latch"},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"MetalBlock","Amount":1},{"Good":"Extract","Amount":1}]}}}}

        # mems[register][bit] = mem

# wire Ms, As, and Os

def set_inputs(target, inputA, inputB):
    target_type = "Memory" if target["Template"] == "Memory.Folktails" else "Relay"
    
    if(inputA != None):
        target["Components"][target_type]["InputA"] = inputA["Id"]
        
    if(inputB != None):
        target["Components"][target_type]["InputB"] = inputB["Id"]

def exists(mapping, register, bit):
    # Okay, gotta make sure a cell actually exists before trying to set anything to it.
    if (mapping.get(register) != None):
        if(mapping[register].get(bit) != None):
            return True
    
    return False

# found earlier: input_bits[] contains all 16 master input bits
# rdo = read_mux["output"]
# wdo = write_mux["output"]
# xdo = exec_mux["output"]

# # just gonna create some blank entries to complete the table
# for register in range(0, 64):
    # for db in (mems, mem_x_a, mem_x_o, mem_r_a, mem_r_o):
        # if(db.get(register) == None):
            # db[register] = {}

# for register in range(0, 64):
    # for bit in range(0, 16):
        # # the mem: reads from the input bit, triggered by wdo. Those will both always exist
        # if(exists(mems, register, bit)):
            # set_inputs(mems[register][bit], input_bits[bit], wdo[register])
        
        # # The other registers... this is where life gets a little interesting
        # if(exists(mem_r_a, register, bit)):
            # set_inputs(mem_r_a[register][bit], rdo[register], mems[register].get(bit))
        
        # if(exists(mem_r_o, register, bit)):
            # set_inputs(mem_r_o[register][bit], mem_r_a[register].get(bit), mem_r_o[register-1].get(bit))
        
        # # The other registers... this is where life gets a little interesting
        # if(exists(mem_x_a, register, bit)):
            # set_inputs(mem_x_a[register][bit], xdo[register], mems[register].get(bit))
        
        # if(exists(mem_x_o, register, bit)):
            # set_inputs(mem_x_o[register][bit], mem_x_a[register].get(bit), mem_x_o[register-1].get(bit))

# hoo boy. Here's hoping we made it through all that!
print("Compiling and writing output")

def dump(mapped):
    for key in mapped:
        all_other_entities.append(mapped[key])

def superdump(meta_map):
    for key in meta_map:
        dump(meta_map[key])

dump(input_bits)
superdump(mems)
superdump(mem_r_a)
superdump(mem_r_o)
#superdump(mem_x_a)
#superdump(mem_x_o)
#superdump(read_mux)

dump(read_mux["output"])
dump(read_mux["internal"])
dump(read_mux["inv_ins"])

#superdump(write_mux)
#superdump(exec_mux)

jason["Entities"] = all_other_entities
out = open("3mux-world-out.json", "w")
json.dump(jason, out)
