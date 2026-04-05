# A two-dimensional vector, for convenient offset work.

class Direction:

  def __init__(self, x, y):
    self._x = x
    self._y = y
  
  def __mul__(self, other):
    if isinstance(other, int):
      newx = self._x * other
      newy = self._y * other
      return Direction(newx, newy)
    else:
      return NotImplemented

  def __add__(self, other):
    if isinstance(other, Direction):
      newx = self._x + other._x
      newy = self._y + other._y
      return Direction(newx, newy)
    else:
      return NotImplemented

class Layout:
  PlusX = Direction(1, 0)
  MinusX = Direction(-1, 0)
  PlusY = Direction(0, 1)
  MinusY = Direction(0, -1)

  def __init__(self, loc, step_dir, row_dir):
    self._loc = loc
    self._step = step_dir
    self._row = row_dir

    self._steps = 0
    self._row_steps = 0

  def loc(self):
    return self._loc
  
  def cursor(self, layer=0):
    step_offset = self._step * self._steps
    row_offset = self._row * self._row_steps
    offset = step_offset + row_offset
    xyz = self._loc
    return(xyz[0] + offset._x, xyz[1]+offset._y, xyz[2] + 2*layer)

  def step(self, steps=1):
    self._steps += steps

  def nextRow(self, steps=1):
    self._steps = 0
    self._row_steps += steps

  def offset(self, steps):
    step_offset = self._step * steps
    row_offset = self._row * self._row_steps
    offset = step_offset + row_offset
    xyz = self._loc
    return (xyz[0]+offset._x, xyz[1]+offset._y, xyz[2])
  
  def clone(self, offset):
    xyz = self._loc
    return Layout((xyz[0]+offset[0], xyz[1]+offset[1], xyz[2]+offset[2]), self._step, self._row)
  
  def starthere(self, offset = 0):
    return Layout(self.cursor(offset), self._step, self._row)
