from src.abstract.node import NodeType, Node
import uuid


class HttpLever(Node):

  def toJson(self):
    return {
      "Id":str(self._id),
      "Template": "HttpLever.Folktails",
      "Components": {
        "NamedEntity":{"EntityName":self._name},
        "BlockObject": {
          "Coordinates":{"X":self._pos[0],"Y":self._pos[1],"Z":self._pos[2]}, 
          "Orientation": "Cw90"
        },
        "Lever": {
        },
        "Automator": {
          "State": "Off"
        },
        "Inventory:ConstructionSite": {
          "Storage": {
            "Goods": [
              {
                "Good": "Gear",
                "Amount": 2
              },
              {
                "Good": "ScrapMetal",
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

    type = NodeType.HTTP_LEVER
    id = uuid.UUID(jason["Id"])
    name = jason["Components"]["NamedEntity"]["EntityName"]
    xyz = (coordinates["X"], coordinates["Y"], coordinates["Z"])
    
    return HttpLever(type, id, name, xyz, None, None, None)