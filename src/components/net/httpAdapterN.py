from src.abstract.component import Component
from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.config.layoutconfig import LayoutConfig
from src.nodes.httpAdapter import HttpAdapter
from src.nodes.httpLever import HttpLever

class HttpAdapterN(Component):
  def __init__(self, name, layout, bits, input, host):
    super().__init__(name, layout)

    self._adaps = []
    for bit in range(bits):
      if(bit > 0 and bit % 8 == 0):
        layout.step(LayoutConfig.ByteSpacing)

      adap = HttpAdapter(NodeType.HTTP_ADAPTER, name + f"_{bit}", layout.cursor(), None, host)
      self._nodes.append(adap)
      self._adaps.append(adap)

      layout.step()

    if input is not None:
      self.setInput(input)

  def setInput(self, input):
    for i in range(len(input._bits)):
      self._adaps[i]._inputA = input._bits[i]
    