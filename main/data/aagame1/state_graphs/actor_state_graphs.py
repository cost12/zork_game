from utils.relator import NameFinder
from models.state import StateGraph, StateGroup

def add_to_name_space(name_space:NameFinder) -> None:
    state_group_inputs = [
        {
            "name"   : "normal",
            "states" : [name_space.get_from_id("normal_character", "state")]
        }
    ]

    state_groups = {inputs['name']: StateGroup(**inputs) for inputs in state_group_inputs}

    state_graph_inputs = [
        {
            "name"          : "standard_character",
            "current_state" : state_groups["normal"]
        }
    ]

    state_graphs = [StateGraph(**inputs) for inputs in state_graph_inputs]

    name_space.add_many(state_graphs)