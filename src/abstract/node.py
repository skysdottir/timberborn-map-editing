from abc import ABC, abstractmethod
from enum import Enum
from uuid import uuid4

class NodeType(Enum):
  RELAY = 100
  RELAY_OR = 101
  RELAY_AND = 102
  RELAY_XOR = 103
  RELAY_NOT = 104
  RELAY_PASSTHROUGH = 105
  MEMORY = 200
  MEM_SET_RESET = 201
  MEM_TOGGLE = 202
  MEM_LATCH = 203
  MEM_FLIPFLOP = 204
  LEVER = 300
  TIMER = 400
  TIMER_DELAY = 401
  TIMER_PULSE = 402
  TIMER_OSCILLATOR = 403
  TIMER_ACCUMULATOR = 404
  INDICATOR = 500
  SENSOR = 600
  SENSOR_FLOW = 601
  SENSOR_DEPTH = 602
  SENSOR_CONTAMINATION = 603
  SENSOR_WEATHER = 604
  SENSOR_POWER = 605
  SENSOR_POPULATION = 606
  SENSOR_RESOURCE = 607
  SENSOR_SCIENCE = 608
  HTTP = 700
  HTTP_LEVER = 701
  HTTP_ADAPTER = 702

class Node(ABC):
  def __init__(self, type, name, pos, inputA=None, inputB=None, inputReset=None):
    self._type = type
    self._id = uuid4()
    self._name = name
    self._pos = pos
    self._inputA = inputA
    self._inputB = inputB
    self._inputReset = inputReset

  # fromJson() is expected to be static
  # It's also currently gonna break horribly on all the node types, don't use it
  # until you've implemented json input correctly
  @abstractmethod
  def fromJson(jason):
    pass

  @abstractmethod
  def toJson():
    pass