from models.actors import Actor, LocationDetail, ItemLimit
from models.state  import State, StateGroup, StateGraph, StateDisconnectedGraph
from utils.relator import NameFinder

from readin.restriction_helpers import Restriction, RestrictionStrategy, RestrictionContext
from readin.description_helpers import Description, ContentsContext, ContentsDescription

def sdg_from_parts(name_space:NameFinder, state_graphs:list[StateGraph]=None, unbreakable_states:list[State]=None, breakable_states:list[State]=None):
    if state_graphs       is None: state_graphs       = []
    if unbreakable_states is None: unbreakable_states = []
    if breakable_states   is None: breakable_states   = []

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

class CharacterRestriction(RestrictionStrategy[Actor]):
    def passes(self, context:RestrictionContext, specific:Actor) -> tuple[bool,Description]:
        return context.character == specific

def get_inventory(character:Actor, item_limit:ItemLimit) -> LocationDetail:
    return LocationDetail(
        name="inventory",
        description_context=ContentsContext("Your inventory contains:", "Your inventory is empty."),
        description_strategy=ContentsDescription(),
        name_id=f"{character.get_name()} inventory",
        aliases=[f"{character.get_name()} inventory"],
        visible_restrictions=[Restriction[Actor](character, CharacterRestriction())],
        item_limit=item_limit,
        size=0,
    )

def get_wearing(character: Actor, item_limit: ItemLimit) -> LocationDetail:
    return LocationDetail(
        name="wearing",
        description_context=ContentsContext("You are wearing:", "You are wearing nothing of note."),
        description_strategy=ContentsDescription(),
        name_id=f"{character.get_name()} wearing",
        aliases=[f"{character.get_name()} wearing"],
        item_limit=item_limit,
        size=0,
    )
