from utils.relator import NameFinder
from models.actors import Target
from models.state import StateDisconnectedGraph, State, StateGraph, StateGroup, Action
from models.response import StaticResponse
from readin.description_helpers import plain_text

def sdg_from_parts(state_graphs:list[StateGraph], unbreakable_states:list[State], breakable_states:list[State], broken_state:State, break_action:Action):
    broken_group = StateGroup(name="Broken", states=[broken_state])
    for state in unbreakable_states:
        state_group = StateGroup(name=state.get_name(), states=[state])
        state_graphs.append(StateGraph(name=state_group.get_name(), current_state=state_group))
    for state in breakable_states:
        state_group = StateGroup(name=state.get_name(), states=[state])
        state_graphs.append(StateGraph(name=f"{state.get_name()} Breakable", current_state=state_group, target_graph={state_group: {break_action: broken_group}}))
    return StateDisconnectedGraph(
        name="sdg",
        state_graphs=state_graphs
    )

def add_to_name_space(name_space:NameFinder) -> None:
    broken_state = name_space.get_from_id("broken", "state")
    break_action = name_space.get_from_id("break", "action")
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable", "stategraph")],
        breakable_states  =[name_space.get_from_id("bouncy",   "state"), 
                            name_space.get_from_id("throwable", "state")],
        breakable_state=broken_state,
        break_action=break_action
    )

    basketball = Target(
        name="Basketball",
        description=(plain_text, "a well-worn basketball"),
        states=sdg,
        weight=2,
        value=3,
        size=3,
        target_responses={name_space.get_from_id("take", "state"): StaticResponse("You can feel many hours of play on the ball's surface")},
        state_responses={name_space.get_from_id("broken", "state"): StaticResponse("The basketball deflates sadly, making itself unusable")}
    )
    
    name_space.add(basketball)