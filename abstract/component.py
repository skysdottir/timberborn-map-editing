# Abstract: A builder for a chunk of timberborn logic.
# Expected workflow: 
# 1) Build a bunch of components, populating their inputs and outputs as you go.
# 2) Validate that they aren't going to collide or otherwise cause trouble
# 3) Sketch() them all, to set up input and output relays, placeholders in-game.
# 4) Do any hand-work in-game
# 5) Come back and Build() to build out the inner workings of all the components.
# 6) Profit!
#
# Components are expected to be nestable

from abc import ABC, abstractmethod

class Component(ABC):
  def __init__(self, loc, dir, input, output):
    self._anchor = loc
    self._directions = dir
    self._input = input
    self._output = output