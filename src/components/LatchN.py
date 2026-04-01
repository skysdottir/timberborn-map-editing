from src.abstract.component import Component
from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.config.layoutconfig import LayoutConfig
from src.nodes.memory import Memory

class LatchN(Component):
  def __init__(self, name, layout, bits, input_word):
    super().__init__(name, layout)
    self._bits = bits

    for bit in range(bits):
      if(bit > 0 and bit % 8 == 0):
        for step in range(LayoutConfig.ByteSpacing):
          layout.step()

      mem = Memory(NodeType.MEM_LATCH, name + f"_{bit}", layout.cursor())
      self._output.bits.append(mem)
      self._nodes.append(mem)

      layout.step()
    
    if input_word is not None:
      self.setInput(input_word)

  def setInput(self, input):
    for bit in range(self._bits):
      self._nodes[bit]._inputA = input._bits[bit]
      self._nodes[bit]._inputB = input._flags[Bus.Enable]