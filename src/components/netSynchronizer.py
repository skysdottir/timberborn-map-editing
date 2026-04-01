from src.abstract.component import Component
from src.abstract.node import NodeType
from src.nodes.httpAdapter import HttpAdapter
from src.nodes.httpLever import HttpLever
from src.nodes.memory import Memory
from src.nodes.relay import Relay

# A simple flag synchronizer for communicating with the outside world
# To the outside world, there's a httpAdapter and a httpLever:
# when adapter XOR lever = 1, it's timber's action, when it's 0 it's the outside world's turn
# Internally, the output's a Node that's high when it's our turn,
# and the input just takes a high pulse to toggle back to the outside turn

class NetSynchronizer(Component):
  def __init__(self, name, loc, input, host):
    super().__init__(name, loc)
    ready = HttpAdapter(NodeType.HTTP_ADAPTER, name+"_ready", loc.cursor(), None, host)
    loc.step()
    used = HttpLever(NodeType.HTTP_LEVER, name+"_used", loc.cursor())
    loc.nextRow()
    myturn = Relay(NodeType.RELAY_XOR, name+"_x", loc.cursor(), ready, used, None)
    loc.step()
    self._mem = Memory(NodeType.MEM_TOGGLE, name+"_m", loc.cursor(), input, None, None)

    self._nodes.extend([ready, used, myturn, self._mem])
    self._output._bits.append(myturn)

  def set_input(self, input):
    self._mem._inputA = input