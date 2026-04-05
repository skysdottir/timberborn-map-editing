from src.abstract.node import NodeType, Node
import uuid

class HttpAdapter(Node):
  def __init__(self, type, name, loc, input, host):
    super().__init__(type, name, loc, input, None, None)
    self._host = host

  def toJson_i(self):
    # No argument will be accepted, POST is the right HTTP verb
    http = {"MethodKey": "Post"}
    # sic "webbook"
    http["SwitchedOnWebbookUrlKey"] = f"http://{self._host}/on/{self._name}"
    http["SwitchedOnWebbookEnabledKey"] = True
    # sic "webbook"
    http["SwitchedOffWebbookUrlKey"] = f"http://{self._host}/off/{self._name}"
    http["SwitchedOffWebbookEnabledKey"] = True

    return {
      "Id":str(self._id),
      "Template": "HttpAdapter.Folktails",
      "Components": {
        "NamedEntity":{"EntityName":self._name},
        "BlockObject": {
          "Coordinates":{"X":self._pos[0],"Y":self._pos[1],"Z":self._pos[2]}, 
          "Orientation": "Cw90"
        },
        "HttpAdapter": http,
        "Automatable": {
          "Input": str(self._inputA._id)
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
                "Amount": 4
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

    switched_on_url = jason["Components"]["HttpAdapter"]["SwitchedOnWebbookUrlKey"]
    switched_off_url = jason["Components"]["HttpAdapter"]["SwitchedOffWebbookUrlKey"]

    type = NodeType.HTTP_LEVER
    id = uuid.UUID(jason["Id"])
    name = jason["Components"]["NamedEntity"]["EntityName"]
    xyz = (coordinates["X"], coordinates["Y"], coordinates["Z"])
    
    return HttpAdapter(type, id, name, xyz, switched_on_url, switched_off_url)