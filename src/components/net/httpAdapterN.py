from src.abstract.component import Component
from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.config.layoutconfig import LayoutConfig
from src.nodes.httpAdapter import HttpAdapter
from src.nodes.httpLever import HttpLever

class HttpAdapterN(Component):
  def __init__(self, name, bits, input, host):
    super().__init__(name, None)

    self._bits = bits
    self._adaps = []
    for bit in range(bits):

      adap = HttpAdapter(NodeType.HTTP_ADAPTER, name + f"_{bit}", None, None, host)
      self._nodes.append(adap)
      self._adaps.append(adap)

    if input is not None:
      self.setInput(input)

  def setInput(self, input):
    for i in range(len(input._bits)):
      self._adaps[i]._inputA = input._bits[i]

  def loc(self, loc):
    for bit in range(self._bits):
      if(bit > 0 and bit % 8 == 0):
        loc.step(LayoutConfig.ByteSpacing)
      self._adaps[bit].loc(loc.cursor())
      loc.step()
    
    return self
    