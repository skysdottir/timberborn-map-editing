# A single bit of memory, for building ram arrays
# Supports 1 read and 1 write simultaneously- no multi-read capabilities here I'm afraid.

from src.abstract.component import Component
from src.abstract.node import NodeType
from src.nodes.memory import Memory
from src.nodes.relay import Relay

class Register1(Component):
  def __init__(self, name, loc, in_value, write_trigger, prev_read, read_trigger):
    super().__init__(name, loc)

    mem_loc = (loc[0], loc[1], loc[2]+4)
    mem = Memory(NodeType.MEM_FLIPFLOP, None, name + "_m", mem_loc, inputAID=str(in_value._id), inputBID=str(write_trigger._id))
    self._nodes.append(mem)

    and_loc = (loc[0], loc[1], loc[2]+2)
    and_relay = Relay(NodeType.RELAY_AND, None, name + "_a", and_loc, str(read_trigger._id), str(mem._id))
    self._nodes.append(and_relay)

    if prev_read is not None:
      or_relay = Relay(NodeType.RELAY_OR, None, name+"_o", loc, str(and_relay._id), str(prev_read._id))
      self._nodes.append(or_relay)
      self._output.bits.append(or_relay)
    else:
      self._output.bits.append(and_relay)
