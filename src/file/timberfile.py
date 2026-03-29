import json
import zipfile
from src.abstract.node import Node
from src.abstract.component import Component

class Timberfile():
  def __init__(self, infile_name, outfile_name):
    self._infile_name = infile_name
    self._outfile_name = outfile_name

    self._entities = []

  def open(self):
    self._in_archive = zipfile.ZipFile(self._infile_name, 'r')
    in_savefile = self._in_archive.open("world.json")
    self._jason = json.load(in_savefile)
    in_savefile.close()

    self._entities = self._jason["Entities"]

  def addEntities(self, ents):
    print("[")
    for entity in ents:
      if isinstance(entity, Node):
        print(json.dumps(entity.toJson()))
        self._entities.append(entity.toJson())

      if isinstance(entity, Component):
        nodes = entity.nodes()
        for node in nodes:
          print(json.dumps(node.toJson()))
          self._entities.append(node.toJson())
      print(",")
    print("]")

  def addJsons(self, jsons):
    self._entities.extend(jsons)

  def save(self):
    # If there's already a zipfile with this name, stomp on it
    out = zipfile.ZipFile(self._outfile_name, "w")

    # Copy the not-changing files
    out.writestr("save_metadata.json", self._in_archive.open("save_metadata.json", 'r').read())
    out.writestr("save_thumbnail.jpg", self._in_archive.open("save_thumbnail.jpg", 'r').read())
    out.writestr("version.txt", self._in_archive.open("version.txt", 'r').read())

    world_string = json.dumps(self._jason)
    out.writestr("world.json", world_string)
    
    out.close()

