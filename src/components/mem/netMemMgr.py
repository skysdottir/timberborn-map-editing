from src.abstract.bus import Bus
from src.abstract.component import Component
from src.abstract.node import NodeType
from src.components.net.httpOutputN import HttpOutputN
from src.components.net.httpLeverN import HttpLeverN
from src.components.net.netSynchronizer import NetSynchronizer
from src.components.busSwitch import BusSwitch
from src.nodes.relay import Relay

# A silly little device for managing a memory block from the network

class NetMemMgr(Component):
  def __init__(self, name, loc, data_bits, addr_bits, pc_read_addr, pc_write_addr, pc_write_bits, host, pc_running=None, mem=None):
    super().__init__(name, loc)

    # The control gates
    pc_read_enable = Relay(NodeType.RELAY_AND, name+"_cr_en", None, pc_running, pc_read_addr._flags[Bus.Enable], None)
    pc_write_enable = Relay(NodeType.RELAY_AND, name+"_cw_en", None, pc_running, pc_write_addr._flags[Bus.Enable], None)
    not_run = Relay(NodeType.RELAY_NOT, name+"_not_run", None, pc_running, None, None)
    self._net_read_enable = Relay(NodeType.RELAY_AND, name+"_nr_en", None, not_run, None, None)
    net_write_enable = Relay(NodeType.RELAY_AND, name+"nw_en", None, not_run, None, None)


    # The synchronizers
    read_sync = NetSynchronizer(name+"_r_sync", None, self._net_read_enable, host)
    write_sync = NetSynchronizer(name+"_w_sync", None, net_write_enable, host)

    self._net_read_enable._inputB = read_sync._output.bits[0]
    net_write_enable._inputB = write_sync._output.bits[0]

    # the net IO
    net_read_addr = HttpLeverN(name+"_ra", addr_bits, host)
    net_read_addr._output._flags[Bus.Enable] = self._read_sync._output.bits[0]

    self._net_read_bits = HttpOutputN(name+"_rb", data_bits, None, host)
    
    net_write_addr = HttpLeverN(name+"_wa", addr_bits, host)
    net_write_bits = HttpLeverN(name+"_wb", data_bits, host)

    # and the switches
    read_addr_switch = BusSwitch(name+"_ras", None, addr_bits, 2)
    write_addr_switch = BusSwitch(name+"_was", None, addr_bits, 2)
    write_bits_switch = BusSwitch(name+"_wbs", None, data_bits, 2)

    read_addr_switch.setInput(net_read_addr._output, 0, self._net_read_enable)
    read_addr_switch.setInput(pc_read_addr, 1, pc_read_enable)

    write_addr_switch.setInput(net_write_addr._output, 0, net_write_enable)
    write_addr_switch.setInput(pc_write_addr, 1, pc_write_enable)

    write_bits_switch.setInput(net_write_bits._output, 0, net_write_enable)
    write_bits_switch.setInput(pc_write_bits, 1, pc_write_enable)

    # save the busses for the memory
    self._mem_read_addr_bus = read_addr_switch._output
    self._mem_write_addr_bus = write_addr_switch._output
    self._mem_write_bits_bus = write_bits_switch._output

    # set locs for everything
    read_sync.loc(loc.starthere())
    loc.step(3)
    read_addr_switch.loc(loc.starthere())
    net_read_addr.loc(loc.starthere(2))

    loc.nextRow(3)

    pc_read_enable.pos(loc.cursor())
    loc.step()
    self._net_read_enable.pos(loc.cursor())
    loc.step(2)
    self._net_read_bits.loc(loc.starthere())

    loc.nextRow()

    not_run.pos(loc.cursor())
    loc.step(3)
    write_bits_switch.loc(loc.starthere())

    loc.nextRow()
    pc_write_enable.loc(loc.cursor())
    loc.step()
    net_write_enable.loc(loc.cursor())

    loc.nextRow(2)
    write_sync.loc(loc.starthere())
    loc.step(3)
    write_addr_switch.loc(loc.starthere())
    net_write_addr.loc(loc.starthere(2))

    # and add them all to self._nodes
    self._nodes.extend([pc_read_enable, pc_write_enable, not_run, self._net_read_enable, net_write_enable])
    self._nodes.extend(net_read_addr._nodes)
    self._nodes.extend(self._net_read_bits)
    self._nodes.extend(net_write_addr._bits)
    self._nodes.extend(net_write_bits._bits)
    self._nodes.extend(read_addr_switch._bits)
    self._nodes.extend(write_addr_switch._bits)
    self._nodes.extend(write_bits_switch._bits)

  def setMem(self, mem):
    mem._output._flags[Bus.Enable] = self._read_sync._output.bits[0]
    self._net_read_bits.input(mem._output, self._net_read_enable)