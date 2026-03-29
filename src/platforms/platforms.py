import uuid

def platform(xyz):
  return {
    "Id":str(uuid.uuid4()),
    "Template":"DoublePlatform.Folktails",
    "Components": 
    {
      "BlockObject": 
      {
        "Coordinates": 
        {
          "X": xyz[0],
          "Y": xyz[1],
          "Z": xyz[2]
        }
      },
      "Inventory:ConstructionSite": 
      {
        "Storage": 
        {
          "Goods": 
          [
            {
              "Good": "Plank",
              "Amount": 8
            }
          ]
        }
      }
    }
  }

def generate_platforms(nodes):
  nodes_xy = {}
  plats = []

  for node in nodes:
    xyz = node._pos
    xy = (xyz[0], xyz[1])

    if nodes_xy.get(xy) is None:
      nodes_xy[xy] = []
    
    nodes_xy[xy].append(node)
  
  for loc, stack in nodes_xy.items():
    print(f"Generating platforms for pos {str(loc)}")
    highest = 0
    
    for node in stack:
      if node._pos[2] > highest:
        highest = node._pos[2]
        print(f"found highest at {highest}")
    
    # super temp code, just assume the map starts at height 4 like the testmap does
    for i in range(4, highest, 2):
      print(f"Generating platform at ({loc[0]}, {loc[1]}, {i})")
      plats.append(platform((loc[0], loc[1], i)))

  return plats