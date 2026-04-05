from src.abstract.node import NodeType, Node
import uuid

class Indicator(Node):

  def toJson_i(self):
    return {
      "Id":str(self._id),
      "Template": "Indicator.Folktails",
      "Components": {
        "NamedEntity":{"EntityName":self._name},
        "BlockObject": {
          "Coordinates":{"X":self._pos[0],"Y":self._pos[1],"Z":self._pos[2]}, 
          "Orientation": "Cw90"
        },
        "Indicator": {
        },
        "Automatable": {
          "Input": str(self._inputA._id)
        },
        "Inventory:ConstructionSite": {
          "Storage": {
            "Goods": [
              {
                "Good": "ScrapMetal",
                "Amount": 2
              },
              {
                "Good": "PineResin",
                "Amount": 1
              }
            ]
          }
        }
      }
    }
  
  @staticmethod
  def fromJson(jason):
    autom = jason["Components"]["Automatable"]
    coordinates = jason["Components"]["BlockObject"]["Coordinates"]

    type = NodeType.INDICATOR
    id = uuid.UUID(jason["Id"])
    name = jason["Components"]["NamedEntity"]["EntityName"]
    xyz = (coordinates["X"], coordinates["Y"], coordinates["Z"])
    inputAID = autom["Input"]
    
    return Indicator(type, id, name, xyz, inputAID, None, None)
