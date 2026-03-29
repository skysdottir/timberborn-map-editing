from src.abstract.node import NodeType
from src.components.register1 import Register1
from src.nodes.lever import Lever
from src.nodes.indicator import Indicator
from src.file.timberfile import Timberfile
from src.platforms.platforms import generate_platforms
import json

import sys

inworld = sys.argv[1]
outworld = sys.argv[2]

file = Timberfile(inworld, outworld)

file.open()

# Generate new components

write_trigger = Lever(NodeType.LEVER, None, "write_trigger", (20, 20, 4), None, None, None)
write_bit = Lever(NodeType.LEVER, None, "write_bit", (22, 20, 4), None, None, None)
prev_read = Lever(NodeType.LEVER, None, "prev_read", (24, 22, 4), None, None, None)
read_trigger = Lever(NodeType.LEVER, None, "read_trigger", (26, 20, 4), None, None, None)

register = Register1("reg", (24, 20, 4), write_bit, write_trigger, prev_read, read_trigger)

# and supporting structures
plats = generate_platforms(register.nodes())

print(json.dumps(plats))

read_indicator = Indicator(NodeType.INDICATOR, None, "read_indicator", (28, 20, 4), str(register.output().bits[0]._id), None, None)

file.addEntities([write_trigger, write_bit, prev_read, read_trigger, register, read_indicator])
file.addJsons(plats)

file.save()