from src.abstract.component import Component
from src.abstract.node import NodeType
from src.abstract.bus import Bus
from src.config.layoutconfig import LayoutConfig
from src.nodes.httpAdapter import HttpAdapter
from src.nodes.httpLever import HttpLever

class HttpLeverN(Component):
  def __init__(self, name, layout, bits, host):
    super().__init__(name, layout)

    ready = HttpLever(NodeType.HTTP_LEVER, name+"_ready", layout.cursor())
    self._nodes.append(ready)
    self._output.flags[Bus.Ready] = ready

    layout.step(2)

    for bit in range(bits):
      if(bit > 0 and bit % 8 == 0):
        layout.step(LayoutConfig.ByteSpacing)

      lever = HttpLever(NodeType.HTTP_LEVER, name + f"_{bit}", layout.cursor())
      self._output.bits.append(lever)
      self._nodes.append(lever)

      layout.step()

    layout.step()
    self._used = HttpAdapter(NodeType.HTTP_ADAPTER, name+"_used", layout.cursor(), None, host)
    self._nodes.append(self._used)

    layout.nextRow()

  # to be called after someone else has set their used flag to our output
  def setUsed(self):
    self._used._inputA = self._output._flags[Bus.Used]