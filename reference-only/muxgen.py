# ! CURRENTLY BUGGED !
# This script is breaking my savefiles when I try to have it generate its own inputs.

# For timberborn computing - generate a demux array (demultiplexes a binary number into N outputs, activates the one from the input)
# "Wideways" and "longways" are (x,y) tuple vectors representing the offset between neighboring cells. They're expected to be neighbors on the map, but knock yourself out.
# "start" is a (x,y) tuple for the coords of output 0. This assumes the area on the map is flat and unoccupied, and does no collision checking.
#
# Eventually: It'll return a map of maps, "input", "output", and "internal". 
#
# Naming:
# Input nodes: [prefix]_i_N
# output nodes: [prefix]_o_N
# internal nodes: [prefix]_[p or n]_X_Y, where X is the output bit and Y is the input bit
#
# How it ends up looking: start is the top left corner, wideways is (1,0), deepways is (0, 1), bits is 3
#
# o0 o1 o2 o3 o4 o5 o6 o7
# -2 -3  2  _ -2  3  2  _
# i0 i1 i2  _ n0 n1 n2  _

import math
import uuid

def get_mux_name(ent):
    if(ent.get("Components") == None or ent["Components"].get("NamedEntity") == None):
        return ""
        
    return ent["Components"]["NamedEntity"]["EntityName"]

def print_relay(relay):
    print(get_mux_name(relay) + ": " + relay["Id"] + " : (" + str(relay["Components"]["BlockObject"]["Coordinates"]["X"]) + ", " + str(relay["Components"]["BlockObject"]["Coordinates"]["Y"]) + ")")
    print(str(relay))
    

def print_mux(mux):
    print("Inputs:")
    for relay in mux["input"]:
        print_relay(mux["input"][relay])
    
    print("Internals:")
    for relay in mux["internal"]:
        print_relay(mux["internal"][relay])
    
    
    print("Outputs:")
    for relay in mux["output"]:
        print_relay(mux["output"][relay])

def make_relay(name, pos, mode, inputA, inputB):
    return {"Id":str(uuid.uuid4()),"Template":"Relay.Folktails","Components":{"NamedEntity":{"EntityName":name},"BlockObject":{"Coordinates":{"X":pos[0],"Y":pos[1],"Z":4}, "Orientation":"Cw90"},"Relay":{"Mode":mode,"InputA":inputA,"InputB":inputB},"Automator":{"State":"Off"},"Inventory:ConstructionSite":{"Storage":{"Goods":[{"Good":"Plank","Amount":1},{"Good":"Gear","Amount":1}]}}}}

def coord(start, wideways, deepways, i, rank):
    u = (wideways[0]*i, wideways[1]*i)
    v = (deepways[0]*rank, deepways[1]*rank)
    x = start[0] + u[0] + v[0]
    y = start[1] + u[1] + v[1]
    z = start[2]
    return (x,y,z)

def mux_recursive_init(ins, inv_ins, prefix, wideways, deepways, nodes, start, start_index, bits):
    width = 2**(bits+1)
    half_width = round(width/2)
    quarter_width = round(width/4)
    
    neg_i = start_index + quarter_width
    neg_name = prefix + "_m_" + str(neg_i)
    neg_loc = coord(start, wideways, deepways, neg_i, 1)
    nodes[neg_i] = make_relay(neg_name, neg_loc, "Passthrough", inv_ins[bits]["Id"], None)
    
    plus_i = start_index + half_width + quarter_width
    plus_name = prefix + "_m_" + str(plus_i)
    plus_loc = coord(start, wideways, deepways, plus_i, 1)
    nodes[plus_i] = make_relay(plus_name, plus_loc, "Passthrough", ins[bits]["Id"], None)
    
    mux_recursive(ins, inv_ins, prefix, wideways, deepways, nodes, start, start_index, bits-1)
    mux_recursive(ins, inv_ins, prefix, wideways, deepways, nodes, start, start_index+half_width, bits-1)

def mux_recursive(ins, inv_ins, prefix, wideways, deepways, nodes, start, start_index, bits):
    if (bits == 0):
        return
    
    width = 2**(bits+1)
    half_width = round(width/2)
    quarter_width = round(width/4)
    
    parent_id = nodes[start_index+half_width]["Id"]
    
    neg_i = start_index + quarter_width
    neg_name = prefix + "_m_" + str(neg_i)
    neg_loc = coord(start, wideways, deepways, neg_i, 1)
    nodes[neg_i] = make_relay(neg_name, neg_loc, "And", parent_id, inv_ins[bits]["Id"])
    
    plus_i = start_index + half_width + quarter_width
    plus_name = prefix + "_m_" + str(plus_i)
    plus_loc = coord(start, wideways, deepways, plus_i, 1)
    nodes[plus_i] = make_relay(plus_name, plus_loc, "And", parent_id, ins[bits]["Id"])
    
    mux_recursive(ins, inv_ins, prefix, wideways, deepways, nodes, start, start_index, bits-1)
    mux_recursive(ins, inv_ins, prefix, wideways, deepways, nodes, start, start_index+half_width, bits-1)

def muxgen(start, wideways, deepways, bits, prefix, inputs):
        outs = {}
        mids = {}
        ins = {}
        inv_ins = {}
        
        mux = [outs, mids, ins]
        
        # starting with the inputs
        offset = 2**(bits-1)
        
        if (inputs == None or len(inputs) == 0):
            #generate placeholder input nodes
            for i in range(bits):
                pos = coord(start, wideways, deepways, i, 0)
                name = prefix + "_i_" + str(i)
                ins[i] = make_relay(name, pos, "Not", None, None)
        else:
            for i in range(bits):
                ins[i] = inputs[i]
        
        offset = bits
        neg_start_coords = (start[0]+offset*wideways[0], start[1]+neg_offset*wideways[1], start[2])
        #And generate the not nodes
        for i in range(bits):
                pos = coord(neg_start_coords, wideways, deepways, i, 0)
                name = prefix + "_n_" + str(i)
                inv_ins[i] = make_relay(name, pos, "Not", ins[i]["Id"], None)
        
        # The recursive mux generation
        mux_recursive_init(ins, inv_ins, prefix, wideways, deepways, mids, start, 0, bits-1)
        
        # And the outputs
        for i in range(2**bits):
            out_name = prefix + "_o_" + str(i)
            out_loc = coord(start, wideways, deepways, i, 2)
            outs[i] = make_relay(out_name, out_loc, "And", mids[(i & 0xFFFE) + 1]["Id"], inv_ins[0]["Id"] if i%2==0 else ins[0]["Id"])
        
        mux = {"output":outs, "input":ins, "internal":mids, "inv_ins":inv_ins}
        return mux
        
        