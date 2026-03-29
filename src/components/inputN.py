from src.abstract.component import Component
from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.config.layoutconfig import LayoutConfig
from src.nodes.lever import Lever

class InputN(Component):
  def __init__(self, name, layout, bits):
    super().__init__(name, layout)

    for bit in range(bits):
      if(bit > 0 and bit % 8 == 0):
        for step in range(LayoutConfig.ByteSpacing):
          layout.step()

      lever = Lever(NodeType.LEVER, None, name + f"_{bit}", layout.cursor())
      self._output.bits.append(lever)
      self._nodes.append(lever)

      layout.step()
    
    layout.nextRow()