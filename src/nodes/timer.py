from src.abstract.node import Node, NodeType

from src.abstract.node import NodeType, Node
import uuid

class Timer(Node):
  type_map = {NodeType.TIMER_ACCUMULATOR: "Accumulator", NodeType.TIMER_OSCILLATOR: "Oscillator", NodeType.TIMER_DELAY: "Delay", NodeType.TIMER_PULSE: "Pulse"}
  to_type_map = {value: key for key, value in type_map.items()}

  def __init__(self, type, name, loc, inputA, inputReset, interval_a_ticks, interval_b_ticks):
    super().__init__(type, name, loc, inputA, None, inputReset)
    self._interval_a = interval_a_ticks
    self._interval_b = interval_b_ticks

  def toJson(self):
    timer = {"Mode":Timer.type_map[self._type]}

    if self._inputA is not None:
      timer["InputA"] = str(self._inputA._id)
    
    if self._inputReset is not None:
       timer["ResetInput"] = str(self._inputReset._id)

    timer["TimerIntervalA"] = {"Type":"Ticks", "Ticks":self._interval_a}

    if(self._type == NodeType.TIMER_OSCILLATOR or self._type == NodeType.TIMER_DELAY):
      timer["TimerIntervalB"] = {"Type":"Ticks", "Ticks":self._interval_b}


    return {
      "Id":str(self._id),
      "Template":"Relay.Folktails",
      "Components":
      {
        "NamedEntity":{"EntityName":self._name},
        "BlockObject":
        {
          "Coordinates":{"X":self._pos[0],"Y":self._pos[1],"Z":self._pos[2]}, 
          "Orientation":"Cw90"
        },
        "Timer": timer,
        "Automator":{"State":"Off"},
        "Inventory:ConstructionSite":
        {
          "Storage":
          {
            "Goods":
            [
              {"Good":"TreatedPlank","Amount":1},
              {"Good":"MetalBlock","Amount":1}
            ]
          }
        }
      }
    }
  
  @staticmethod
  def fromJson(jason):
    timer = jason["Components"]["Timer"]
    coordinates = jason["Components"]["BlockObject"]["Coordinates"]

    type = Timer.to_type_map[jason["Components"]["Timer"]["Mode"]]
    id = uuid.UUID(jason["Id"])
    name = jason["Components"]["NamedEntity"]["EntityName"]
    xyz = (coordinates["X"], coordinates["Y"], coordinates["Z"])
    inputAID = uuid.UUID(timer["InputA"])
    inputResetID = uuid.UUID(timer["ResetInput"])
    interval_a = timer["TimerIntervalA"]["Ticks"]
    interval_b = timer["TimerIntervalB"]["Ticks"]

    return Timer(type, id, name, xyz, inputAID, inputResetID, interval_a, interval_b)
