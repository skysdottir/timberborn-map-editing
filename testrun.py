from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.components.memoryBank import MemoryBank
from src.components.netMemMgr import NetMemMgr
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

nmm = NetMemMgr("nmm", Layout((20, 20, 4), Layout.PlusY, Layout.PlusX), bits, address_bits, "localhost:8081")

memory = MemoryBank("mem", Layout((26, 20, 4), Layout.PlusY, Layout.PlusX), nmm._read_addr_bus, nmm._write_addr_bus, nmm._write_bits_bus, bits, address_bits)

nmm.setMem(memory)

# and supporting structures
plats = generate_platforms(memory.nodes())

file.addEntities([nmm, memory])
file.addJsons(plats)

file.save()