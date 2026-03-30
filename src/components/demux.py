from src.abstract.component import Component
from src.abstract.node import NodeType
from src.nodes.relay import Relay
from src.abstract.bus import Bus

# Note: This assumes you're always looking for a power of two.
# How it ends up looking:
# o0 o1 o2 o3 o4 o5 o6 o7
# -2 -3  2  _ -2  3  2  _
# z0 i0 i1 i2 n0 n1 n2  _

def mux_recursive(bits, inputs, inv_inputs, start_index, name, parent, layout, ret):
  # end condition, there's only one bit left to divide.
  if(bits == 1):
    return
  
  width = 2**bits
  half_width = round(width/2)
  quarter_width = round(width/4)

  low_index = start_index + quarter_width - 1
  high_index = start_index + half_width + quarter_width - 1

  low = Relay(NodeType.RELAY_PASSTHROUGH, name+"_m_"+str(low_index), layout.offset(low_index), inv_inputs[bits-1], None, None)
  high = Relay(NodeType.RELAY_PASSTHROUGH, name+"_m_"+str(high_index), layout.offset(high_index), inputs[bits-1], None, None)
  
  if parent is not None:
    low._type = NodeType.RELAY_AND
    low._inputB = parent
    high._type = NodeType.RELAY_AND
    high._inputB = parent
  
  ret[low_index] = low
  ret[high_index] = high

  mux_recursive(bits-1, inputs, inv_inputs, start_index, name, low, layout, ret)
  mux_recursive(bits-1, inputs, inv_inputs, start_index+half_width, name, high, layout, ret)

  return ret

class Demux(Component):
  def __init__(self, name, layout, bits, in_bus):
    super().__init__(name, layout)

    zero_replacement = Relay(NodeType.RELAY_AND, name+"_ze", layout.cursor(), in_bus._flags[Bus.Enable], None, None)
    self._nodes.append(zero_replacement)

    self.inputs_and_enable = []

    for i in range(bits):
      layout.step()
      relay = Relay(NodeType.RELAY_AND, name+"_in_"+str(i), layout.cursor(), in_bus._flags[Bus.Enable], in_bus._bits[i], None)
      self.inputs_and_enable.append(relay)
      self._nodes.append(relay)
    
    self.inverse_ins = []

    for i in range(bits):
      layout.step()
      relay = Relay(NodeType.RELAY_NOT, name+"_ni_"+str(i), layout.cursor(), self.inputs_and_enable[i], None, None)
      self.inverse_ins.append(relay)
      self._nodes.append(relay)
    
    # Up next: the recursive demux
    layout.nextRow()

    ints = {}
    mux_recursive(bits, self.inputs_and_enable, self.inverse_ins, 0, name, None, layout, ints)
    self._nodes.extend(ints.values())

    # And the output row
    layout.nextRow()

    for i in range(0, 2**bits, 2):
      parent = ints[i]
      low = Relay(NodeType.RELAY_AND, name+"_out_"+str(i), layout.cursor(), parent, self.inverse_ins[0], None)
      self._nodes.append(low)
      self._output._bits.append(low)
      layout.step()
      high = Relay(NodeType.RELAY_AND, name+"_out_"+str(i+1), layout.cursor(), parent, self.inputs_and_enable[0], None)
      self._nodes.append(high)
      self._output._bits.append(high)
      layout.step()

    # And finally, the special handling for 0 when we're not enabled
    zero_and_enable = self._output._bits[0]
    zero_replacement._inputA = zero_and_enable._inputA
    zero_replacement._inputB = zero_and_enable._inputB
    zero_and_enable._inputA = zero_replacement
    zero_and_enable._inputB = in_bus._flags[Bus.Enable]

    # And a final bump to the layout
    layout.nextRow()
