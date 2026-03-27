# An input or output bus for a component

# bits: [] of data nodes
# flags: {} of flag bits
# Common flags:
## Enable = these bits are for this unit of logic. Expected synchronously with data.
## Shift = shift signal for shift registers
## Ready = Half of a signal-flag pair, for asynch buffers
## Used = The other half of a signal-flag pair.

# Ready/Used are a signaling pair: Ready XOR Used will give bus status:
## 0: Waiting for the inputter to send next bits
## 1: Waiting for the reader to consume the current bits

class Bus:
  def __init__(self, bits, flags):
    self._bits = []
    self._flags = {}

    for bit in bits:
      self._bits.append(bit)
    for flag in flags:
      self._flags[flag] = flags[flag]

  @property
  def populated(self):
    return (self.width() > 0)
  
  @property
  def width(self):
    return len(self._bits)
  
  @property
  def bits(self):
    return self._bits
  
  @property
  def flags(self):
    return self._flags
  
  @bits.setter
  def bits(self, bits):
    self._bits = bits
