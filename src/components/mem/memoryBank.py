from src.abstract.component import Component
from src.abstract.layout import Layout
from src.components.mem.registerN import RegisterN
from src.components.demux import Demux
from src.config.layoutconfig import LayoutConfig

# A big old memory bank for all your memory banking needs
# Currently only supports register counts that are 2**n
# Because Demux has that limitation

class MemoryBank(Component):
  def __init__(self, name, loc, read_address, write_address, write_bits, bit_count, address_bits):
    super().__init__(name, loc)

    self._write_demux = Demux(name+"_wd", Layout(loc._loc, loc._step, loc._row), address_bits, write_address)
    self._read_demux = Demux(name+"_rd", Layout((loc._loc[0], loc._loc[1], loc._loc[2]+2), loc._step, loc._row), address_bits, read_address)
    self._nodes.extend(self._write_demux._nodes)
    self._nodes.extend(self._read_demux._nodes)

    loc.nextRow(steps = 4)
    self._registers = []

    lastReg = None

    for i in range(2**address_bits):
      reg = RegisterN(name+"_"+str(i), Layout(loc.cursor(), loc._row, loc._step), bit_count, write_bits, self._write_demux._output._bits[i], None if lastReg is None else lastReg._output, self._read_demux._output._bits[i])
      loc.step()
      self._nodes.extend(reg._nodes)
      lastReg = reg
      self._output = reg._output