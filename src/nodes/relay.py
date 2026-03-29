from src.abstract.node import NodeType, Node
import uuid

class Relay(Node):
  type_map = {NodeType.RELAY_OR: "Or", NodeType.RELAY_AND: "And", NodeType.RELAY_XOR: "Xor", NodeType.RELAY_NOT: "Not", NodeType.RELAY_PASSTHROUGH: "Passthrough"}
  to_type_map = {value: key for key, value in type_map.items()}

  def toJson(self):
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
        "Relay":
        {
          "Mode":Relay.type_map[self._type],
          "InputA":self._inputAID,
          "InputB":self._inputBID
        },
        "Automator":{"State":"Off"},
        "Inventory:ConstructionSite":
        {
          "Storage":
          {
            "Goods":
            [
              {"Good":"Plank","Amount":1},
              {"Good":"Gear","Amount":1}
            ]
          }
        }
      }
    }
  
  @staticmethod
  def fromJson(jason):
    relay = jason["Components"]["Relay"]
    coordinates = jason["Components"]["BlockObject"]["Coordinates"]

    type = Relay.to_type_map[jason["Components"]["Relay"]["Mode"]]
    id = uuid.UUID(jason["Id"])
    name = jason["Components"]["NamedEntity"]["EntityName"]
    xyz = (coordinates["X"], coordinates["Y"], coordinates["Z"])
    inputAID = uuid.UUID(relay["InputA"])

    inputBID = None
    if not (type == NodeType.RELAY_NOT or NodeType.RELAY_PASSTHROUGH):
      inputBID = uuid.UUID(relay["InputB"])

    return Relay(type, id, name, xyz, inputAID, inputBID, None)
