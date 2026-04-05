from src.abstract.component import Component
from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.config.layoutconfig import LayoutConfig
from src.nodes.memory import Memory

class LatchN(Component):
  def __init__(self, name, bits, input_word, layout=None):
    super().__init__(name, layout)
    self._bits = bits

    for bit in range(bits):
      mem = Memory(NodeType.MEM_LATCH, name + f"_{bit}")
      self._output.bits.append(mem)
      self._nodes.append(mem)

      layout.step()
    
    if input_word is not None:
      self.setInput(input_word)

    if layout is not None:
      self.loc(layout)

  def setInput(self, input):
    for bit in range(self._bits):
      self._nodes[bit]._inputA = input._bits[bit]
      self._nodes[bit]._inputB = input._flags[Bus.Enable]

  def loc(self, loc):
    for bit in range(self._bits):
      if(bit > 0 and bit % 8 == 0):
        loc.step(LayoutConfig.ByteSpacing)
      self._nodes[bit].loc(loc.cursor())
      loc.step()
    
    return self