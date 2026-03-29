# A single register N bits wide, for configurable N.
# Powers of 2 are traditional, but knock yourself out!
# Built from register1, so, supports th same IO count

from src.abstract.component import Component


class Register1(Component):
  def __init__(self, name, loc, dir, in_value, write_trigger, prev_read, read_trigger):
    super().__init__(name, loc, dir)


  def dimensions(self):
    xyz = self._anchor
    xyz2 = (xyz[0], xyz[1], xyz[2]+4)
    return (xyz, xyz2)