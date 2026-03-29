from src.abstract.component import Component
from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.config.layoutconfig import LayoutConfig
from src.nodes.indicator import Indicator

class IndicatorN(Component):
  def __init__(self, name, layout, bits, input):
    super().__init__(name, layout)

    for bit in range(bits):
      if(bit > 0 and bit % 8 == 0):
        for step in range(LayoutConfig.ByteSpacing):
          layout.step()

      indic = Indicator(NodeType.INDICATOR, None, name + f"_{bit}", layout.cursor(), input.bits[bit])
      self._nodes.append(indic)

      layout.step()
    
    layout.nextRow()