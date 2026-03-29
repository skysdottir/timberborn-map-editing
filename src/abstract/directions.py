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
    
PlusX = Direction(1, 0)
MinusX = Direction(-1, 0)
PlusY = Direction(0, 1)
MinusY = Direction(0, -1)

class Layout:
  def __init__(self, loc, step_dir, row_dir):
    self._loc = loc
    self._step = step_dir
    self._row = row_dir

    self._steps = 0
    self._row_steps = 0

  def loc(self):
    return self._loc
  
  def cursor(self):
    step_offset = self._step_dir * self._steps
    row_offset = self._row_dir * self._rows
    offset = step_offset + row_offset
    xyz = self._loc
    return(xyz[0] + offset._x, xyz[1]+offset._y, xyz[2])

  def step(self):
    self._steps += 1

  def nextRow(self):
    self._steps = 0
    self._row_steps += 1
