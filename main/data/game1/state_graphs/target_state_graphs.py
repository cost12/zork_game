from utils.relator import NameFinder
from models.state import StateGraph, StateGroup

def add_to_name_space(name_space:NameFinder) -> None:
    state_group_inputs = [
        {"name": "breakable",       "states": ["breakable"], "name_id":"breakable (group)"},
        {"name": "broken",          "states": ["broken"]},
        {"name": "held",            "states": ["held"]},
        {"name": "held_wearable",   "states": ["held", "wearable"]},
        {"name": "takeable",        "states": ["takeable"], "name_id": "takeable (group)"},
        {"name": "off",             "states": ["off", "breakable"]},
        {"name": "broken_off",      "states": ["off", "broken"]},
        {"name": "on",              "states": ["on", "breakable"]},
        {"name": "flammable",       "states": ["flammable"], "name_id": "flammable (group)"},
        {"name": "on fire",         "states": ["on fire"]},
        {"name": "burned",          "states": ["burned"]},
        {"name": "opened",          "states": ["opened"]},
        {"name": "closed",          "states": ["closed"]},
        {"name": "broken_open",     "states": ["opened", "broken"]},
        {"name": "locked",          "states": ["locked", "closed"], "name_id": "locked (group)"},
        {"name": "unlocked_closed", "states": ["unlocked", "closed"]},
        {"name": "unlocked_open",   "states": ["unlocked", "opened"]},
        {"name": "wearable",        "states": ["wearable", "takeable"], "name_id": "wearable (group)"},
        {"name": "worn",            "states": ["worn", "takeable"]},
        {"name": "tied",            "states": ["tied"]},
        {"name": "untied",          "states": ["untied"]},
        {"name": "full",            "states": ["full"]},
        {"name": "empty",           "states": ["empty (state)"]},
        {"name": "broken_empty",    "states": ["empty (state)", "broken"]}
    ]

    for inputs in state_group_inputs: # being lazy - replacing states ids with objects
        inputs['states'] = [name_space.get_from_id(state, "state") for state in inputs['states']]

    state_groups = {inputs.get('name_id', inputs['name']): StateGroup(**inputs) for inputs in state_group_inputs}

    state_graph_inputs = [
        {
            "name"            : "container sg",
            "current_state"   : "empty",
            "target_graph"    : {
                "empty"       : {
                    "fill"    : "full",
                    "break"   : "broken_empty"
                },
                "full"        : {
                    "empty"   : "empty",
                    "break"   : "broken_empty"
                }
            }
        },
        {
            "name"            : "fragile_untie sg",
            "current_state"   : "tied",
            "target_graph"    : {
                "tied"        : {
                    "untie"   : "untied"
                }
            }
        },
        {
            "name"            : "wearable sg",
            "current_state"   : "wearable (group)",
            "target_graph"    : {
                "wearable (group)" : {
                    "wear"    : "worn",
                    "take"    : "held_wearable",
                    "break"   : "takeable (group)"
                },
                "worn"        : {
                    "take off": "wearable (group)",
                    "take"    : "held_wearable"            
                },
                "held_wearable" : {
                    "drop"    : "wearable (group)",
                    "wear"    : "worn",
                    "break"   : "held"
                },
                "takeable (group)" : {
                    "take"    : "held"
                },
                "held"        : {
                    "drop"    : "takeable (group)"
                }
            }
        },
        {
            "name"            : "locked sg",
            "current_state"   : "locked (group)",
            "target_graph"    : {
                "locked (group)"      : {
                    "unlock"  : "unlocked_closed",
                    "break"   : "broken_open"
                },
                "unlocked_closed" : {
                    "open"    : "unlocked_open",
                    "lock"    : "locked (group)",
                    "break"   : "broken_open"
                },
                "unlocked_open" : {
                    "close"   : "unlocked_closed",
                    "lock"    : "locked (group)",
                    "break"   : "broken_open"
                }
            }
        },
        {
            "name"            : "open_close sg",
            "current_state"   : "closed",
            "target_graph"    : {
                "opened"      : {
                    "close"   : "closed",
                    "break"   : "broken_open"
                },
                "closed"      : {
                    "open"    : "opened",
                    "break"   : "broken_open"
                }
            }
        },
        {
            "name"            : "lightable sg",
            "current_state"   : "flammable (group)",
            "target_graph"    : {
                "flammable (group)"   : {
                    "burn"   :"on fire"
                },
                "on fire"     : {
                    "extinguish": "flammable (group)"
                }
            }
        },
        {
            "name"            : "flammable sg",
            "current_state"   : "flammable (group)",
            "target_graph"    : {
                "flammable (group)"   : {
                    "burn"   : "on fire"
                },
                "on fire"     : {
                    "extinguish": "burned"
                }
            },
            "time_graph"      : {
                "on fire"     : [3, "burned"]
            }
        },
        {
            "name"            : "breakable sg",
            "current_state"   : "breakable (group)",
            "target_graph"    : {
                "breakable (group)"   : {
                    "break"   : "broken"
                }
            }
        },
        {
            "name"            : "takeable sg",
            "current_state"   : "takeable (group)",
            "target_graph"    : {
                "takeable (group)"    : {
                    "take"    : "held"
                },
                "held"        : {
                    "drop"    : "takeable (group)"
                }
            }
        },
        {
            "name"            : "switch sg",
            "current_state"   : "off",
            "target_graph"    : {
                "off"         : {
                    "toggle"  : "on",
                    "turn on" : "on",
                    "break"   : "broken_off"
                },
                "on"          : {
                    "toggle"  : "off",
                    "turn off": "off",
                    "break"   : "broken_off"
                }
            }
        }
    ]

    for inputs in state_graph_inputs: # being lazy - replacing state group/ action ids with objects
        inputs["current_state"] = state_groups[inputs['current_state']]
        if 'target_graph' in inputs:
            inputs['target_graph'] = {
                state_groups[state_group] : {
                    name_space.get_from_id(action, "action") : state_groups[state_group2] for action, state_group2 in state_dict.items()
                } for state_group, state_dict in inputs['target_graph'].items()
            }
        if 'time_graph' in inputs:
            inputs['time_graph'] = {
                state_groups[state_group] : [time_state[0], state_groups[time_state[1]]] for state_group, time_state in inputs['time_graph'].items()
            }

    state_graphs = [StateGraph(**inputs) for inputs in state_graph_inputs]

    name_space.add_many(state_graphs)
