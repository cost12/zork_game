from utils.relator import NameFinder
from models.named import Direction

def add_to_name_space(name_space:NameFinder) -> None:
    direction_inputs = [
        {"name"    : "any",       "aliases" : ["any"]},
        {"name"    : "north",     "aliases" : ["north", "n"]},
        {"name"    : "northwest", "aliases" : ["northwest", "nw"]},
        {"name"    : "west",      "aliases" : ["west", "w"]},
        {"name"    : "southwest", "aliases" : ["southwest", "sw"]},
        {"name"    : "south",     "aliases" : ["south", "s"]},
        {"name"    : "southeast", "aliases" : ["southeast", "se"]},
        {"name"    : "east",      "aliases" : ["east", "e"]},
        {"name"    : "northeast", "aliases" : ["northeast", "ne"]},
        {"name"    : "up",        "aliases" : ["up", "u"]},
        {"name"    : "down",      "aliases" : ["down", "d"]},
        {"name"    : "out",       "aliases" : ["out"]},
        {"name"    : "in trunk",  "aliases" : ["in trunk"]},
        {"name"    : "in car",    "aliases" : ["in car"]}
    ]

    directions = [Direction(**inputs) for inputs in direction_inputs]

    name_space.add_many(directions)
