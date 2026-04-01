from src.abstract.node import NodeType, Node
import uuid

class Memory(Node):
  type_map = {NodeType.MEM_SET_RESET: "SetReset", NodeType.MEM_TOGGLE: "Toggle", NodeType.MEM_LATCH: "Latch", NodeType.MEM_FLIPFLOP: "FlipFlop"}
  to_type_map = {value: key for key, value in type_map.items()}

  def toJson(self):
    mem = {"Mode":Memory.type_map[self._type]}

    if self._inputA is not None:
      mem["InputA"] = str(self._inputA._id)
    
    if self._inputB is not None:
       mem["InputB"] = str(self._inputB._id)

    if self._inputReset is not None:
      mem["ResetInput"] = str(self._inputReset._id)


    return {
      "Id":str(self._id),
      "Template":"Memory.Folktails",
      "Components":
      {
        "NamedEntity":{"EntityName":self._name},
        "BlockObject":
        {
          "Coordinates":{"X":self._pos[0],"Y":self._pos[1],"Z":self._pos[2]}
        },
        "Memory": mem,
        "Automator":{"State":"Off"},
        "Inventory:ConstructionSite":
        {
          "Storage":
          {
            "Goods":
            [
              {"Good":"MetalBlock","Amount":1},
              {"Good":"Extract","Amount":1}
            ]
          }
        }
      }
    }
  
  @staticmethod
  def fromJson(jason):
    memory = jason["Components"]["Memory"]
    coordinates = jason["Components"]["BlockObject"]["Coordinates"]

    type = Memory.to_type_map[jason["Components"]["Memory"]["Mode"]]
    id = uuid.UUID(jason["Id"])
    name = jason["Components"]["NamedEntity"]["EntityName"]
    xyz = (coordinates["X"], coordinates["Y"], coordinates["Z"])
    inputAID = uuid.UUID(memory["InputA"])

    inputBID = None
    if type == NodeType.MEM_LATCH or type == NodeType.MEM_FLIPFLOP:
      inputBID = uuid.UUID(memory["InputB"])

    inputResetID = uuid.UUID(memory["InputReset"])

    return Memory(type, id, name, xyz, inputAID, inputBID, inputResetID)
