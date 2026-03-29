from src.abstract.node import NodeType
from src.components.register1 import Register1
from src.components.registerN import RegisterN
from src.components.inputN import InputN
from src.components.indicatorN import IndicatorN
from src.nodes.lever import Lever
from src.file.timberfile import Timberfile
from src.platforms.platforms import generate_platforms
from src.abstract.Layout import Layout
import json

import sys

inworld = sys.argv[1]
outworld = sys.argv[2]

file = Timberfile(inworld, outworld)
file.open()

# Generate new components
bits = 16
write_trigger = Lever(NodeType.LEVER, None, "write_trigger", (20, 18, 4), None, None, None)
write_bits = InputN("write_bit", Layout((20, 20, 4), Layout.PlusY, Layout.PlusX), bits)
read_trigger = Lever(NodeType.LEVER, None, "read_trigger", (22, 18, 4), None, None, None)

register = RegisterN("reg", Layout((22, 20, 4), Layout.PlusY, Layout.PlusX), bits, write_bits.output(), write_trigger, None, read_trigger)

# and supporting structures
plats = generate_platforms(register.nodes())

print(json.dumps(plats))

read_indicator = IndicatorN("indicator", Layout((24, 20, 4), Layout.PlusY, Layout.PlusX), bits, register.output())

file.addEntities([write_trigger, write_bits, read_trigger, register, read_indicator])
file.addJsons(plats)

file.save()