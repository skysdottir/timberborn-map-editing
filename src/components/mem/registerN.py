# A single register N bits wide, for configurable N.
# Powers of 2 are traditional, but knock yourself out!
# Built from register1, so, supports th same IO count

from src.abstract.component import Component
from src.components.mem.register1 import Register1
from src.config.layoutconfig import LayoutConfig

class RegisterN(Component):
  def __init__(self, name, layout, bits, in_word, write_trigger, prev_read_word, read_trigger):
    super().__init__(name, layout)

    for bit in range(bits):
      if(bit > 0 and bit % 8 == 0):
        for step in range(LayoutConfig.ByteSpacing):
          layout.step()
          
      reg = Register1(name + f"_{bit}", layout.cursor(), in_word._bits[bit], write_trigger, None if prev_read_word is None else prev_read_word._bits[bit], read_trigger)
      self._nodes.extend(reg._nodes)
      self._output.bits.append(reg._output.bits[0])

      layout.step()
    
    layout.nextRow()