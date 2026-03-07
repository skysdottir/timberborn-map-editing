Timberborn map editing scripts for building computers

Warning! This voids your warranty. This will break your save-files, and leave you to try to sort out the mess. Always back things up, and don't file crash reports. Here there be dragons. If you haven't played Timberborn until you're bored of it at least once, maybe just go back to the game instead of messing with this stuff.

This package is very much a work-in-progress. Use it (except maybe timbercheck.py) as reference, not tooling. It contains bugs. It will build unloadable maps. Some of these scripts were built for very situation-specific tasks, and I keep them around for reference's sake.

Now- some advice:

1) A .timber file is really just a .zip. Rename it, unzip it, and inside it you'll find world.json, the actual save file. It's big, but don't be intimidated- it's really very clean, readable, editable json. If you walk the dark path you will spend a lot of time reading world.json, either completely by hand or with your favorite text-search tool.

2) The most important elements of an entity for timber computing are:

entity["Id"]: the UUID identifier of the entity. As far as I can tell, this is just a type-4 UUID, so, totally random.
entity["Components"]["NamedEntity"]["EntityName"]: The human-readable name of the entity. Give your relays and memories meaningful names, it will make digging through a json for why things broke so much easier.
entity["Components"]["BlockObject"]["Coordinates"]: the X/Y/Z coordinates of the entity
entity["Components"]["Relay" or "Memory"]: The subtype of the entity (AND, OR, Latch, Flip-Flop, etc), and its inputs' UUIDs

3) Never overwrite your input file. You will need multiple loops of the run script -> try to load -> troubleshoot cycle, maintaining the exact same input is incredibly helpful.

4) Have a test map. Make it as simple as you possibly can.

5) Always run timbercheck.py. It's probably the most reliable script here - if it complains, pay attention, and try to understand why it's complaining.

These scripts do not currently understand terrain. Timbercheck.py understands locations enough to check for entity collisions, but the other scripts do not. They will just plop things down where specified and crash the game.