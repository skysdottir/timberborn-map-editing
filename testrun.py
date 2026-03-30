from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.components.memoryBank import MemoryBank
from src.components.inputN import InputN
from src.components.indicatorN import IndicatorN
from src.nodes.lever import Lever
from src.file.timberfile import Timberfile
from src.platforms.platforms import generate_platforms
from src.abstract.layout import Layout

import sys

inworld = sys.argv[1]
outworld = sys.argv[2]

file = Timberfile(inworld, outworld)
file.open()

# Generate new components
bits = 8
address_bits = 4

write_enable = Lever(NodeType.LEVER, "write_trigger", (20, 20, 4), None, None, None)
write_addr_bits = InputN("write_addr", Layout((20, 22, 4), Layout.PlusY, Layout.PlusX), address_bits)
write_addr_bits._output._flags[Bus.Enable] = write_enable

write_bits = InputN("write_bits", Layout((22, 20, 4), Layout.PlusY, Layout.PlusX), bits)

read_enable = Lever(NodeType.LEVER, "read_trigger", (24, 20, 4), None, None, None)
read_addr_bits = InputN("write_addr", Layout((24, 22, 4), Layout.PlusY, Layout.PlusX), address_bits)
read_addr_bits._output._flags[Bus.Enable] = read_enable

memory = MemoryBank("mem", Layout((28, 20, 4), Layout.PlusY, Layout.PlusX), read_addr_bits._output, write_addr_bits._output, write_bits._output, bits, address_bits)

display = IndicatorN("indic", Layout((26, 20, 4), Layout.PlusY, Layout.PlusX), bits, memory._output)

# and supporting structures
plats = generate_platforms(memory.nodes())

file.addEntities([write_enable, write_addr_bits, write_bits, read_enable, read_addr_bits, display, memory])
file.addJsons(plats)

file.save()