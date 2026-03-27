from enum import Enum

class Type(Enum):
  RELAY = 100
  RELAY_OR = 101
  RELAY_AND = 102
  RELAY_XOR = 103
  RELAY_NOT = 104
  MEMORY = 200
  MEM_SET_RESET = 201
  MEM_TOGGLE = 202
  MEM_LATCH = 203
  MEM_FLIPFLOP = 204
  LEVER = 300
  TIMER = 400
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

class Node:
  def __init__(self, type, loc, inputA, inputB, inputReset):
    self._type = type
    self._loc = loc
    self._inputA = inputA
    self._inputB = inputB
    self._inputReset = inputReset
