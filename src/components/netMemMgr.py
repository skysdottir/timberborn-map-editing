from src.abstract.bus import Bus
from src.abstract.component import Component
from src.abstract.node import NodeType
from src.components.httpAdapterN import HttpAdapterN
from src.components.httpLeverN import HttpLeverN
from src.nodes.memory import Memory
from src.nodes.relay import Relay

# A silly little device for managing a memory block from the network

# The read process:
# Both read_addr and read_bits start ready to write, read_enable starts off
# network writes read addr
# network writes read_addr_ready, **read_enable goes high**
# mem reads, writes back to read_bits
# read_bits_ready goes high, **read_enable stays high**
# network reads bits
# network writes read_bits_used, read_bits go back to ready, read_addr_used goes high, read_addr goes back to ready, **read_enable goes low**
# And we're back where we started, just with both _ready and _useds high instead of low

# read_addr_status = read_addr_ready xor read_addr_used
# read_bit_status = read_bits_ready xor read_bits_used
# not_read_bit_status = !read_bit_status
# read_enable = memory, sets on read_addr_status, resets on not_read_bit_status
# read_addr_used = memory, toggles on not read_bit_status
# read_bits_ready = memory, toggles on mem read

class NetMemMgr(Component):
  def __init__(self, name, loc, data_bits, addr_bits, host, mem=None):
    super().__init__(name, loc)

    # Create the nodes, do none of the wiring until we have the Memory we're managing

    # When both the read bits have been consumed and the read addr has been set
    # read_addr_status will be 1 (ready for consumption)
    # read_status will be 0 (ready for input)

    self._read_addr_status = Relay(NodeType.RELAY_XOR, name+"_ra_x", loc.cursor())
    loc.step()
    self._read_bits_status = Relay(NodeType.RELAY_XOR, name+"_rb_x", loc.cursor())
    loc.step()
    self._not_read_bits_status = Relay(NodeType.RELAY_NOT, name+"rb_n", loc.cursor(), self._read_bits_status, None, None)

    loc.step(2)

    self._read_addr = HttpLeverN(name+"_ra", loc, addr_bits, host)

    self._nodes.extend([self._read_addr_status, self._read_bits_status, self._not_read_bits_status])
    self._nodes.extend(self._read_addr._nodes)

    self._read_enable = Memory(NodeType.MEM_SET_RESET, name+"_read", loc.cursor(), self._read_addr_status, None, self._not_read_bits_status)
    loc.step()
    self._read_addr_used = Memory(NodeType.MEM_TOGGLE, name+"_ra_u", loc.cursor(), self._not_read_bits_status, None, None)
    loc.step()
    self._read_bits_ready = Memory(NodeType.MEM_TOGGLE, name+"_rb_r", loc.cursor(), self._read_enable, None, None)
    loc.step(2)

    self._read_bits = HttpAdapterN(name+"_rb", loc, data_bits, None, host)

    self._nodes.extend([self._read_enable, self._read_addr_used, self._read_bits_ready])
    self._nodes.extend(self._read_bits._nodes)
    loc.nextRow()

    # Populate the read flags that we can
    self._read_addr_bus = self._read_addr._output
    self._read_bits_status._inputB = self._read_bits_ready
    # And once we have the memory's output bus, we need to set:
    # read_ready_toggle -> ready
    # mem out bus -> read_bits in bus
    # mem out bus [Used] -> self._read_bits_status._inputA


    # read address, bus from read_addr httpLevers to memory module with some extra shenanigans in the middle to phase shift from synch to asynch
    self._read_addr_status._inputA = self._read_addr_bus._flags[Bus.Ready]
    self._read_addr_status._inputB = self._read_addr_used
    self._read_addr_bus._flags[Bus.Enable] = self._read_enable
    self._read_addr_bus._flags[Bus.Used] = self._read_addr_used
    self._read_addr.setUsed()
    

    # When both the write bits and write address have been set
    # write_addr_status will be 1 (ready for consumption)
    # write_bit_status will be 1 (ready for consumption)
    write_addr_status = Relay(NodeType.RELAY_XOR, name+"_wa_x", loc.cursor())
    loc.step()
    write_bits_status = Relay(NodeType.RELAY_XOR, name+"_wb_x", loc.cursor())
    loc.step(3)

    write_addr = HttpLeverN(name+"_wa", loc, addr_bits, host)

    self._nodes.extend([write_addr_status, write_bits_status])
    self._nodes.extend(write_addr._nodes)

    # We'll tell the mem to write
    # and then the mem will delay a tick before setting both write and write_addr Useds
    write_enable = Relay(NodeType.RELAY_AND, name+"_read", loc.cursor(), write_addr_status, write_bits_status)
    loc.step()
    write_used_toggle = Memory(NodeType.MEM_TOGGLE, name+"_wb_m", loc.cursor(), write_enable, None, None)
    loc.step(3)

    write_bits = HttpLeverN(name+"_wb", loc, data_bits, host)

    self._nodes.extend([write_enable, write_used_toggle])
    self._nodes.extend(write_bits._nodes)

    # set up the write busses
    self._write_addr_bus = write_addr._output
    self._write_addr_bus._flags[Bus.Enable] = write_enable
    self._write_addr_bus._flags[Bus.Used] = write_used_toggle
    write_addr.setUsed()
    write_addr_status._inputA = self._write_addr_bus._flags[Bus.Ready]
    write_addr_status._inputB = write_used_toggle

    self._write_bits_bus = write_bits._output
    self._write_bits_bus._flags[Bus.Enable] = write_enable
    self._write_bits_bus._flags[Bus.Used] = write_used_toggle
    write_bits.setUsed()
    write_bits_status._inputA = self._write_bits_bus._flags[Bus.Ready]
    write_bits_status._inputB = write_used_toggle

    # And if we were constructed with a mem, jump to the wiring
    if mem is not None:
      self.setMem(mem)
  
  # set this manager's memory - and wire up the remaining relays
  def setMem(self, mem):
    output = mem._output
    output._flags[Bus.Ready] = self._read_bits_ready
    self._read_bits.setInput(output)
    self._read_bits_status._inputA = output._flags[Bus.Used]

