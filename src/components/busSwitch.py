from src.abstract.component import Component
from src.abstract.bus import Bus
from src.abstract.node import NodeType
from src.nodes.relay import Relay

# Switches output between N input busses, based on their enable bits
# Assumes there's only one enable bit set at a time
# Makes a two-tall stack of relays, ANDS over ORs (just like memoryBank)
# It's busWidth+2 wide (bits + space + enable bit)
# and count long
# And it will successfully ignore missing inputs

class BusSwitch(Component):
  def __init__(self, name, loc, busWidth, count):
    super().__init__(name, loc)

    self._inputs = []
    self._ors = []
    self._ands = []
    self._enable_ors = [None]

    for i in range(count):
      ands = []
      ors = []
      for bit in range(busWidth):
        ands.append(Relay(NodeType.RELAY_AND, name+f"_a_{i}_{bit}", loc.cursor(layer=1)))

        if count != 0:
          ors.append(Relay(NodeType.RELAY_OR, name+f"_o_{i}_{bit}", loc.cursor(), ands[bit], self._output._bits[bit], None))
        loc.step()

      self._nodes.extend(ands)
      self._nodes.extend(ors)
      loc.step()
      
      if count != 0:
        en_or = Relay(NodeType.RELAY_OR, name+f"_o_{i}_en", loc.cursor(), self._enable_ors[i-1], None, None)
        self._enable_ors.append(en_or)
        self._nodes.append(en_or)
        self._output._bits = ors
        self._output._flags[Bus.Enable] = en_or
      else:
        self._output._bits = ands

      loc.nextRow()
  
  def setInput(self, inputBus, index):
    for bit in range(len(inputBus._bits)):
      self._ands[index][bit]._inputA = inputBus._flags[Bus.Enable]
      self._ands[index][bit]._inputB = inputBus._bits[bit]
      
    if index == 0:
      self._enable_ors[1]._inputA = inputBus._flags[Bus.Enable]
    else:
      self._enable_ors[index]._inputB = inputBus._flags[Bus.Enable]
