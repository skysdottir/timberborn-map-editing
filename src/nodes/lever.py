from src.abstract.node import NodeType, Node
import uuid

class Lever(Node):

  def toJson(self):
    return {
      "Id":str(self._id),
      "Template": "Lever.Folktails",
      "Components": {
        "NamedEntity":{"EntityName":self._name},
        "BlockObject": {
          "Coordinates":{"X":self._pos[0],"Y":self._pos[1],"Z":self._pos[2]}, 
          "Orientation": "Cw90"
        },
        "Lever": {
          "IsSpringReturn": False,
          "IsPinned": False
        },
        "Automator": {
          "State": "Off"
        },
        "Inventory:ConstructionSite": {
          "Storage": {
            "Goods": [
              {
                "Good": "Plank",
                "Amount": 1
              },
              {
                "Good": "Gear",
                "Amount": 2
              }
            ]
          }
        }
      }
    }
  
  @staticmethod
  def fromJson(jason):
    lever = jason["Components"]["Lever"]
    coordinates = jason["Components"]["BlockObject"]["Coordinates"]

    type = NodeType.LEVER
    id = uuid.UUID(jason["Id"])
    name = jason["Components"]["NamedEntity"]["EntityName"]
    xyz = (coordinates["X"], coordinates["Y"], coordinates["Z"])
    
    return Lever(type, id, name, xyz, None, None, None)
