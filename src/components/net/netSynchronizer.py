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
    self._ready = HttpAdapter(NodeType.HTTP_ADAPTER, name+"_ready", None, None, host)
    self._used = HttpLever(NodeType.HTTP_LEVER, name+"_used", None)
    
    self._mem = Memory(NodeType.MEM_TOGGLE, name+"_m", None, input, None, None)
    self._myturn = Relay(NodeType.RELAY_XOR, name+"_x", None, self._mem, self._used, None)
    self._ready._inputA = self._mem

    self._nodes.extend([self._ready, self._used, self._myturn, self._mem])
    self._output._bits.append(self._myturn)

    if loc is not None: self.set_loc(loc)

  def set_input(self, input):
    self._mem._inputA = input

  def loc(self, loc):
    self._ready.pos(loc.cursor())
    loc.step()
    self._used.pos(loc.cursor())
    loc.nextRow()
    self._mem.pos(loc.cursor())
    loc.step()
    self._myturn.pos(loc.cursor())

    return self