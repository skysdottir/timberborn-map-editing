from src.abstract.bus import Bus
from src.abstract.component import Component
from src.abstract.layout import Layout
from src.abstract.node import NodeType
from src.components.httpAdapterN import HttpAdapterN
from src.components.httpLeverN import HttpLeverN
from src.components.netSynchronizer import NetSynchronizer
from src.nodes.memory import Memory
from src.nodes.relay import Relay

# A silly little device for managing a memory block from the network
# still todo: Wiring it up so it can also work with a computer internally
# right now it's just external-facing

class NetMemMgr(Component):
  def __init__(self, name, loc, data_bits, addr_bits, host, mem=None):
    super().__init__(name, loc)

    read_sync = NetSynchronizer(name+"_r_sync", Layout(loc.cursor(), loc._step, loc._row), None, host)

    # Just loopback the input, we're going to read immediately when we're triggered and pass it back
    read_sync.set_input(read_sync._output.bits[0])

    loc.step(3)
    read_addr = HttpLeverN(name+"_ra", loc, addr_bits, host)
    self._read_addr_bus = read_addr._output
    self._read_addr_bus.flags[Bus.Enable] = read_sync._output.bits[0]

    loc.nextRow()
    loc.step(3)
    read_bits = HttpAdapterN(name+"_rb", loc, data_bits, None, host)
    self._read_bits = read_bits

    loc.nextRow(2)

    write_sync = NetSynchronizer(name+"_w_sync", Layout(loc.cursor(), loc._step, loc._row), None, host)

    # Also just loopback the input, we're going to write immediately when triggered and pass control back
    write_sync.set_input(write_sync._output.bits[0])

    loc.step(3)
    write_addr = HttpLeverN(name+"_wa", loc, addr_bits, host)
    self._write_addr_bus = write_addr._output
    self._write_addr_bus.flags[Bus.Enable] = write_sync._output.bits[0]

    loc.nextRow()
    loc.step(3)
    write_bits = HttpLeverN(name+"_wb", loc, data_bits, host)
    self._write_bits_bus = write_bits._output

    self._nodes.extend(read_sync._nodes)
    self._nodes.extend(read_addr._nodes)
    self._nodes.extend(read_bits._nodes)
    self._nodes.extend(write_sync._nodes)
    self._nodes.extend(write_addr._nodes)
    self._nodes.extend(write_bits._nodes)

  def setMem(self, mem):
    self._read_bits.setInput(mem._output)