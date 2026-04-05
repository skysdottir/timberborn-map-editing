from src.components.net.httpOutputN import HttpOutputN
from src.components.LatchN import LatchN
from src.abstract.bus import Bus
from src.nodes.relay import Relay
from src.abstract.node import NodeType
from src.abstract.component import Component
from src.abstract.layout import Layout


# A disablable http output widget
class HttpOutputN(Component):
  def __init__(self, name, bits, input, host):
    super().__init__(name, None)

    self._ands = Bus()
    for i in range(bits):
      self._ands._bits.append(Relay(NodeType.RELAY_AND, f"_a_{i}", None))
    
    self._mems = LatchN(name+"_m", bits, self._ands)
    self._adaps = HttpOutputN(name+"_o", bits, self._mems._output, host)

    if input is not None:
      self.input(input)

    self._nodes.extend(self._ands._bits)
    self._nodes.extend(self._mems._nodes)
    self._nodes.extend(self._adaps._nodes)
  
  def input(self, input, enable = None):
    en = input._flags[Bus.Enable] if enable is None else enable
    for node in self._ands._bits:
      node._inputA = input._bits[i]
      node._inputB = en

  def loc(self, loc):
    self._mems.loc(Layout(loc.cursor(1), loc._step, loc._row))
    self._adaps.loc(Layout(loc.cursor(2), loc._step, loc._row))

    for node in self._ands._bits:
      node.pos(loc.cursor())
      loc.step()
    
    return self

  