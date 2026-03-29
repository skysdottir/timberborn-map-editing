# Abstract: A builder for a chunk of timberborn logic.
# Expected workflow: 
# 1) Build a bunch of components
# 1.5) Partially as you go and partially after the fact, set inputs and outputs
# 2) Validate that they aren't going to collide or otherwise cause trouble
# 3) Sketch() them all, to set up input and output relays, placeholders in-game.
# 4) Do any hand-work in-game
# 5) Come back and Build() to build out the inner workings of all the components.
# 6) Profit!
#
# Components are expected to be nestable

from abc import ABC, abstractmethod
from src.abstract.bus import Bus

class Component(ABC):
  def __init__(self, name, loc):
    self._name = name
    self._anchor = loc

    self._output = Bus([], {})
    self._nodes = []
    self._subcomponents = []

  # Returns all the entities this component needs
  def nodes(self):
    back = []

    for subcomp in self._subcomponents:
      back.extend(subcomp.nodes())
    
    back.extend(self._nodes)

    return back
  
  def output(self):
    return self._output