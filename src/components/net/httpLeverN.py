from src.abstract.component import Component
from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.config.layoutconfig import LayoutConfig
from src.nodes.httpAdapter import HttpAdapter
from src.nodes.httpLever import HttpLever

class HttpLeverN(Component):
  def __init__(self, name, bits, host):
    super().__init__(name, None)

    for bit in range(bits):
      lever = HttpLever(NodeType.HTTP_LEVER, name + f"_{bit}")
      self._output.bits.append(lever)
      self._nodes.append(lever)

  def loc(self, loc):
    for bit in range(self._bits):
      if(bit > 0 and bit % 8 == 0):
        loc.step(LayoutConfig.ByteSpacing)
      self._nodes[bit].loc(loc.cursor())
      loc.step()
    
    return self