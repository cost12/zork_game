from utils.relator import NameFinder
from models.state import State

def add_to_name_space(name_space:NameFinder) -> None:
    state_inputs = [
        {
            "name"             : "normal_character",
            "actions_as_actor" : frozenset([
                "look",
                "take",
                "drop",
                "hang",
                "inventory",
                "wearing",
                "wait",
                "walk",
                "break",
                "turn on",
                "turn off",
                "toggle",
                "attack",
                "play",
                "conduct",
                "eat",
                "drink",
                "dig",
                "wear",
                "take off",
                "shoot",
                "bounce",
                "give",
                "burn",
                "extinguish",
                "unlock",
                "lock",
                "open",
                "close",
                "say",
                "arm wrestle",
                "work on",
                "read",
                "type",
                "tie",
                "untie",
                "fill",
                "empty",
                "admire",
                "squeeze",
                "ride",
                "perform",
                "lift",
                "pour",
                "hug",
                "kiss",
                "compliment"
            ]),
            "actions_as_target": frozenset(["look", "attack", "arm wrestle"])
        },
        {
            "name" : "guarding"
        }
    ]

    for inputs in state_inputs: # being lazy - replacing action ids with Action objects
        for category in ["actions_as_target", "actions_as_tool", "actions_as_actor"]:
            if category in inputs:
                inputs[category] = [name_space.get_from_id(action, "action") for action in inputs[category]]

    states = [State(**inputs) for inputs in state_inputs]

    name_space.add_many(states)
