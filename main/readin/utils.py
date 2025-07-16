from models.state  import State, StateGroup, StateGraph, StateDisconnectedGraph
from models.named  import Action
from utils.relator import NameFinder

def sdg_from_parts(state_graphs:list[StateGraph], unbreakable_states:list[State], breakable_states:list[State], name_space:NameFinder):
    broken_state = name_space.get_from_id("broken", "state")
    break_action = name_space.get_from_id("break", "action")
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