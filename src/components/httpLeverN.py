from src.abstract.component import Component
from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.config.layoutconfig import LayoutConfig
from src.nodes.httpAdapter import HttpAdapter
from src.nodes.httpLever import HttpLever

class HttpLeverN(Component):
  def __init__(self, name, layout, bits, host):
    super().__init__(name, layout)

    for bit in range(bits):
      if(bit > 0 and bit % 8 == 0):
        layout.step(LayoutConfig.ByteSpacing)

      lever = HttpLever(NodeType.HTTP_LEVER, name + f"_{bit}", layout.cursor())
      self._output.bits.append(lever)
      self._nodes.append(lever)

      layout.step()