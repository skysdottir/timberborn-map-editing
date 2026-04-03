from src.abstract.bus import Bus
from src.abstract.component import Component
from src.abstract.node import NodeType
from src.abstract.layout import Layout
from src.components.net.httpAdapterN import HttpAdapterN
from src.components.net.httpLeverN import HttpLeverN
from src.components.LatchN import LatchN
from src.components.net.netSynchronizer import NetSynchronizer
from src.nodes.relay import Relay

# A silly little device for managing a memory block from the network

# So - the levers might be left in any state by the external programmer
# If the computer is running, I need to hard ignore those.
# And likewise I should hard ignore any computer input when the computer isn't running
# For all inputs, then, I need to...
# AND RUN and pc-enable bits
# AND (NOT RUN) and net-enable bits
# AND enablers and bus bits
# OR each input bus together for throughput to the memory unit
# output is simpler:
# AND read synchronizer's output bit and (NOT RUN)
# Use that to toggle the read synchronizer's enable bit instead of plumbing it directly from the output bit
# Set master_enable as reset for the read store

class NetMemMgr(Component):
  def __init__(self, name, loc, data_bits, addr_bits, pc_read_addr, pc_write_addr, pc_write_bits, host, pc_running=None, mem=None):
    super().__init__(name, loc)

    # read_sync's input will be set to the net_read_enable bit later
    read_sync = NetSynchronizer(name+"_r_sync", loc.clone(), None, host)
    self._read_sync = read_sync

    loc.step(4)
    read_addr = HttpLeverN(name+"_ra", loc, addr_bits, host)
    self._read_addr_bus = read_addr._output
    self._read_addr_bus.flags[Bus.Enable] = read_sync._output.bits[0]

    loc.nextRow()
    # row 2 of the read NetSynchronizer
    loc.step(4)
    self._read_store = LatchN(name+"_rm", loc, data_bits, None)

    loc.nextRow()
    self._pc_read_enable = Relay(NodeType.RELAY_AND, name+"_cr_en", loc.cursor(), pc_running, pc_read_addr._flags[Bus.Enable], None)
    loc.step()
    self._not_run = Relay(NodeType.RELAY_NOT, name+"_not_run", loc.cursor(), pc_running, None, None)
    loc.step()
    self._net_read_enable = Relay(NodeType.RELAY_AND, name+"_nr_en", loc.cursor(), self._not_run, read_sync._output.bits[0])
    read_sync.set_input(self._net_read_enable)
    loc.step(2)

    read_bits = HttpAdapterN(name+"_rb", loc, data_bits, self._read_store._output, host)
    self._read_bits = read_bits

    loc.nextRow(2)

    write_sync = NetSynchronizer(name+"_w_sync", loc.clone(), None, host)

    # Also just loopback the input, we're going to write immediately when triggered and pass control back
    write_sync.set_input(write_sync._output.bits[0])

    loc.step(4)
    write_addr = HttpLeverN(name+"_wa", loc, addr_bits, host)
    self._write_addr_bus = write_addr._output
    self._write_addr_bus.flags[Bus.Enable] = write_sync._output.bits[0]

    loc.nextRow()
    # Row 2 of the write NetSynchronizer
    loc.step(4)
    write_bits = HttpLeverN(name+"_wb", loc, data_bits, host)
    self._write_bits_bus = write_bits._output

    self._nodes.extend(read_sync._nodes)
    self._nodes.extend(read_addr._nodes)
    self._nodes.extend(read_bits._nodes)
    self._nodes.extend(self._read_store._nodes)
    self._nodes.extend(write_sync._nodes)
    self._nodes.extend(write_addr._nodes)
    self._nodes.extend(write_bits._nodes)

  def setMem(self, mem):
    mem._output._flags[Bus.Enable] = self._read_sync._output.bits[0]
    self._read_store.setInput(mem._output)