from typing import Optional, Any, Callable

from models.named       import Named, Action, Direction
from models.actors      import ItemLimit, HasLocation, Location, Path, Target, Actor, LocationDetail, SingleEndPath, MultiEndPath, Achievement
from models.requirement import ActionRequirement, CharacterAchievementRequirement, CharacterStateRequirement, ItemsHeldRequirement, ItemStateRequirement, ItemPlacementRequirement
from models.state       import State, StateGroup, StateGraph, StateDisconnectedGraph, Skill, SkillSet
from models.response    import ResponseString, StaticResponse, CombinationResponse, ItemStateResponse, ContentsResponse, RandomResponse, ContentsWithStateResponse
from controls.character_control import CharacterController, CommandLineController, NPCController

# REQUIREMENTS

def character_state_requirements_from_dict(name:str, requirement_dict:dict[str,Any], state_factory:'StateFactory') -> CharacterStateRequirement:
    states_needed = dict[State,tuple[bool,ResponseString]]()
    for state_name, needed in requirement_dict.items():
        state = state_factory.get_state(state_name)
        if state is None:
            print(f"Can't find state {state_name} in {name}")
        if isinstance(needed, bool):
            states_needed[state] = (needed,None)
        else:
            states_needed[state] = (needed[0], StaticResponse(needed[1]))
    return CharacterStateRequirement(states_needed)

def character_achievement_requirements_from_dict(name:str, requirement_dict:dict[str,Any], achievement_factory:'NamedFactory[Achievement]') -> CharacterAchievementRequirement:
    achievements_needed = dict[Achievement,tuple[bool,ResponseString]]()
    for achievement_name, needed in requirement_dict.items():
        achievement = achievement_factory.get_named(achievement_name)
        if achievement is None:
            print(f"Can't find achievement {achievement_name} in {name}")
        if isinstance(needed, bool):
            achievements_needed[achievement] = (needed,None)
        else:
            achievements_needed[achievement] = (needed[0], StaticResponse(needed[1]))
    return CharacterAchievementRequirement(achievements_needed)

def item_state_requirements_from_dict(name:str, requirement_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory', state_factory:'StateFactory') -> ItemStateRequirement:
    item_states = dict[Target,dict[State,tuple[bool,ResponseString]]]()
    for item_name, states_needed_raw in requirement_dict.items():
        item = item_factory.get_item(item_name)
        if item is None:
            item = character_factory.get_character(item_name)
        if item is None:
            print(f"Can't find target {item_name} in {name}")
        states_needed = dict[State,tuple[bool,str]]()
        for state_name, needed in states_needed_raw.items():
            state = state_factory.get_state(state_name)
            if state is None:
                print(f"Can't find state {state_name} in {name}")
            if isinstance(needed, bool):
                states_needed[state] = (needed,None)
            else:
                states_needed[state] = (needed[0], StaticResponse(needed[1]))
        item_states[item] = states_needed
    return ItemStateRequirement(item_states)

def item_placement_requirements_from_dict(name:str, requirement_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory', location_factory:'LocationFactory', detail_factory:'LocationDetailFactory') -> ItemPlacementRequirement:
    item_placements = dict[Target,list[tuple[Location,bool,ResponseString]]]()
    for item_name, location_info in requirement_dict.items():
        item = item_factory.get_item(item_name)
        if item is None:
            item = character_factory.get_character(item_name)
        if item is None:
            print(f"Can't find target {item_name} in {name}")
        placements = list[tuple[Location,bool,ResponseString]]()
        for location_name, needed, response in location_info:
            location = location_factory.get_location(location_name)
            if location is None:
                location = detail_factory.get_detail(location_name)
            if location is None:
                print(f"Can't find location {location_name} in {name}")
            placements.append((location, needed, StaticResponse(response)))
        item_placements[item] = placements
    return ItemPlacementRequirement(item_placements)

def items_held_requirement_from_dict(name:str, requirement_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory') -> ItemsHeldRequirement:
    items_needed = dict[Target,tuple[bool,ResponseString]]()
    for item_name, needed in requirement_dict.items():
        item = item_factory.get_item(item_name)
        if item is None:
            item = character_factory.get_character(item_name)
        if item is None:
            print(f"Can't find target {item_name} in {name}")
        if isinstance(needed, bool):
            items_needed[item] = (needed,None)
        else:
            items_needed[item] = (needed[0], ResponseString(needed[1]))
    return ItemsHeldRequirement(items_needed)

def requirements_from_dict(name:str, requirements_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory', state_factory:'StateFactory', achievement_factory:'NamedFactory[Achievement]', location_factory:'LocationFactory', detail_factory:'LocationDetailFactory') -> list[ActionRequirement]:
    requirements = list[ActionRequirement]()
    if 'character_state_requirements' in requirements_dict:
        states_needed_raw = requirements_dict['character_state_requirements']
        requirements.append(character_state_requirements_from_dict(name, states_needed_raw, state_factory))
    if 'character_achievement_requirements' in requirements_dict:
        achievements_needed_raw = requirements_dict['character_achievement_requirements']
        requirements.append(character_achievement_requirements_from_dict(name, achievements_needed_raw, achievement_factory))
    if 'item_state_requirements' in requirements_dict:
        item_states_raw = requirements_dict['item_state_requirements']
        requirements.append(item_state_requirements_from_dict(name, item_states_raw, item_factory, character_factory, state_factory))
    if 'items_held_requirements' in requirements_dict:
        items_needed_raw = requirements_dict['items_held_requirements']
        requirements.append(items_held_requirement_from_dict(name, items_needed_raw, item_factory, character_factory))
    if 'item_placement_requirements' in requirements_dict:
        item_placements_raw = requirements_dict['item_placement_requirements']
        requirements.append(item_placement_requirements_from_dict(name, item_placements_raw, item_factory, character_factory, location_factory, detail_factory))
    return requirements     

# RESPONSES

def contents_response_from_dict(name:str, response_dict:dict[str,str], item_factory:'ItemFactory', character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory') -> ContentsResponse:
    target_name = name
    if 'target' in response_dict:
        target_name = response_dict['target']
    target = item_factory.get_item(target_name)
    if target is None: target = character_factory.get_character(target_name)
    if target is None: target = detail_factory.get_detail(target_name)
    if target is None: print(f"Can't find target {target_name} in {name} response")
    full_response  = response_dict.get('full', None)
    if full_response is None: print(f"Error missing full response in {name}")
    empty_response = response_dict['empty']
    return ContentsResponse(full_response, empty_response, target)

def contents_with_state_response_from_dict(name:str, response_dict:dict[str,str|dict[str,str]], item_factory:'ItemFactory', character_factory:'CharacterFactory', state_factory:'StateFactory') -> ItemStateResponse:
    target_name = name
    if 'target' in response_dict:
        target_name = response_dict.get('target', None)
    target = item_factory.get_item(target_name)
    if target is None: target = character_factory.get_character(target_name)
    if target is None: print(f"Can't find target {target_name} in {name} response")
    responses = dict[State,str]()
    for state_name, response in response_dict['responses'].items():
        state = state_factory.get_state(state_name)
        if state is None: print(f"Can't find state {state_name} in {name} response")
        responses[state] = response
    default = response_dict.get('default', None)
    return ContentsWithStateResponse(target, responses, default=default)

def item_state_response_from_dict(name:str, response_dict:dict[str,str|dict[str,str]], item_factory:'ItemFactory', character_factory:'CharacterFactory', state_factory:'StateFactory') -> ItemStateResponse:
    target_name = name
    if 'target' in response_dict:
        target_name = response_dict.get('target', None)
    target = item_factory.get_item(target_name)
    if target is None: target = character_factory.get_character(target_name)
    if target is None: print(f"Can't find target {target_name} in {name} response")
    responses = dict[State,str]()
    for state_name, response in response_dict['responses'].items():
        state = state_factory.get_state(state_name)
        if state is None: print(f"Can't find state {state_name} in {name} response")
        responses[state] = response
    default = response_dict.get('target', None)
    return ItemStateResponse(target, responses, default=default)

def random_response_from_list(name, response_list:list[str|dict], item_factory:'ItemFactory', character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory', location_factory:'LocationFactory', state_factory:'StateFactory', action_factory:'NamedFactory[Action]', achievement_factory:'NamedFactory[Achievement]') -> RandomResponse:
    responses = list[ResponseString]()
    for response in response_list:
        responses.append(response_from_input(name, response, item_factory, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory))
    return RandomResponse(responses)

def response_from_list(name:str, input_list:list[str|dict[str,Any]], item_factory:'ItemFactory', character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory', location_factory:'LocationFactory', state_factory:'StateFactory', action_factory:'NamedFactory[Action]', achievement_factory:'NamedFactory[Achievement]') -> CombinationResponse:
    responses = list[ResponseString]()
    for response in input_list:
        responses.append(response_from_input(name, response, item_factory, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory))
    return CombinationResponse(responses)

def response_from_dict(name:str, response_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory', location_factory:'LocationFactory', state_factory:'StateFactory', action_factory:'NamedFactory[Action]', achievement_factory:'NamedFactory[Achievement]') -> ResponseString:
    match response_dict['type']:
        case 'item_state':
            return item_state_response_from_dict(name, response_dict, item_factory, character_factory, state_factory)
        case 'contents':
            return contents_response_from_dict(name, response_dict, item_factory, character_factory, detail_factory)
        case 'contents_with_state':
            return item_state_response_from_dict(name, response_dict, item_factory, character_factory, state_factory)
        case 'random':
            return random_response_from_list(name, response_dict['responses'], item_factory, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
        case _:
            print(f'In {name} unknown response type {response_dict['type']}')

def response_from_input(name:str, input:str|dict[str,Any]|list, item_factory:'ItemFactory', character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory', location_factory:'LocationFactory', state_factory:'StateFactory', action_factory:'NamedFactory[Action]', achievement_factory:'NamedFactory[Achievement]') -> ResponseString:
    if isinstance(input, str):
        return StaticResponse(input)
    elif isinstance(input, list):
        return response_from_list(name, input, item_factory, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
    elif isinstance(input, dict):
        return response_from_dict(name, input, item_factory, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)

# OTHER RESPONSES

def item_responses_from_dict(name:str, response_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory', location_factory:'LocationFactory', state_factory:'StateFactory', action_factory:'NamedFactory[Action]', achievement_factory:'NamedFactory[Achievement]') -> dict['HasLocation',str]:
    responses = dict[HasLocation,ResponseString]()
    for item_name, response in response_dict:
        item = item_factory.get_item(item_name)
        if item is None:
            item = character_factory.get_character(item_name)
        if item is None:
            print(f"Can't find target {item_name} in {name}")
        responses[item] = response_from_input(name, response, item_factory, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
    return responses

def action_responses_from_dict(name:str, response_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory', location_factory:'LocationFactory', state_factory:'StateFactory', action_factory:'NamedFactory[Action]', achievement_factory:'NamedFactory[Achievement]') -> dict[Action,str]:
    responses = dict[Action,ResponseString]()
    for action_name, response in response_dict.items():
        action = action_factory.get_named(action_name)
        if action is None:
            print(f"Can't find action {action_name} in {name}")
        responses[action] = response_from_input(name, response, item_factory, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
    return responses

def state_responses_from_dict(name:str, response_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory', location_factory:'LocationFactory', state_factory:'StateFactory', action_factory:'NamedFactory[Action]', achievement_factory:'NamedFactory[Achievement]') -> dict[State,str]:
    responses = dict[State,ResponseString]()
    for state_name, response in response_dict.items():
        state = state_factory.get_state(state_name)
        if state is None:
            print(f"Can't find state {state_name} in {name}")
        responses[state] = response_from_input(name, response, item_factory, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
    return responses

def direction_responses_from_dict(name:str, response_dict:dict[str,Any], direction_factory:'NamedFactory[Direction]', item_factory:'ItemFactory', character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory', location_factory:'LocationFactory', state_factory:'StateFactory', action_factory:'NamedFactory[Action]', achievement_factory:'NamedFactory[Achievement]') -> dict[Direction,str]:
    responses = dict[Direction,ResponseString]()
    for direction_name, response in response_dict.items():
        direction = direction_factory.get_named(direction_name)
        if direction is None:
            print(f"Can't find direction {direction_name} in {name}")
        responses[direction] = response_from_input(name, response, item_factory, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
    return responses

# OTHER HELPERS

def children_from_dict(name, children_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory'=None) -> dict[str,HasLocation]:
    children = dict[str,HasLocation]()
    for item_name in children_dict:
        item = item_factory.get_item(item_name)
        if item is None:
            item = character_factory.get_character(item_name)
        if item is None and detail_factory is not None:
            item = detail_factory.get_detail(item_name)
        if item is None:
            print(f"Can't find target {item_name} in {name}")
        children[item.get_name()] = item
    return children

def item_limit_from_dict(limit_dict:dict[str,Any]) -> ItemLimit:
    size   = limit_dict.get('size',   None)
    weight = limit_dict.get('weight', None)
    value  = limit_dict.get('value',  None)
    return ItemLimit(size_limit=size, weight_limit=weight, value_limit=value)

def path_from_dict(path_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory', state_factory:'StateFactory', achievement_factory:'NamedFactory[Achievement]') -> Path:
        name = path_dict['name']
        end = path_dict.get('end', None)
        path_type = None
        if 'end' in path_dict:
            path_type = 'restricted'
        if 'multi_end' in path_dict:
            path_type = 'multi'
            multi_end = dict[Target, str]()
            for item_name, room_name in path_dict['multi_end'].items():
                item = item_factory.get_item(item_name)
                if item is None:
                    print(f"Can't find item {item_name} in {name}")
                multi_end[item] = room_name
        if path_type is None:
            print(f"ERROR: path {name} has no type")
        hidden_when_locked = path_dict.get('hidden_when_locked', False)
        exit_response = path_dict.get('exit_response', None)
        item_limit = item_limit_from_dict(path_dict['item_limit']) if 'item_limit' in path_dict else None
        aliases = path_dict.get('aliases', None)
        if path_type == 'restricted':
            return SingleEndPath(name, None, end=end, item_limit=item_limit, exit_response=exit_response, hidden_when_locked=hidden_when_locked, aliases=aliases)
        elif path_type == 'multi':
            return MultiEndPath(name, None, end=end, multi_end=multi_end, item_limit=item_limit, exit_response=exit_response, hidden_when_locked=hidden_when_locked, aliases=aliases)

def sdg_from_dict(name:str, sgd_dict:dict[str,list[str]], state_factory:'StateFactory', graph_factory:'StateGraphFactory', action_factory:'NamedFactory[Action]') -> StateDisconnectedGraph:
    state_graphs = list[StateGraph]()
    if "states" in sgd_dict:
        for state_name in sgd_dict["states"]:
            state = state_factory.get_state(state_name)
            if state is None:
                print(f"Can't find state {state_name} in SDG for {name}")
            state_group = StateGroup(state.get_name(), [state])
            state_graphs.append(StateGraph(state_group.get_name(), state_group))
    if "breakable" in sgd_dict:
        breakable_states = list[State]()
        for state_name in sgd_dict["breakable"]:
            state = state_factory.get_state(state_name)
            if state is None:
                print(f"Can't find state {state_name} in SDG for {name}")
        state_group = StateGroup(f"{name}_breakable", breakable_states)
        break_action = action_factory.get_named("break")
        if break_action is None:
            print(f"Can't find action break in SDG for {name}")
        broken_state = state_factory.get_state("broken")
        if broken_state is None:
            print(f"Can't find state broken in SDG for {name}")
        broken_group = StateGroup("broken", [broken_state])
        target_graph = {state_group: {break_action: broken_group}}
        state_graphs.append(StateGraph(f"{name}_breakable", state_group, target_graph=target_graph))
    if "graphs" in sgd_dict:
        for graph_name in sgd_dict["graphs"]:
            graph = graph_factory.get_state_graph(graph_name)
            if graph is None:
                print(f"Can't find state graph {graph_name} in SDG for {name}")
            state_graphs.append(graph)
    return StateDisconnectedGraph(name, state_graphs)

def inventory_from_dict(name:str, inventory_dict:dict[str,Any], item_factory:'ItemFactory', character_factory:'CharacterFactory') -> LocationDetail:
    item_limit = None
    if 'item_limit' in inventory_dict:
        item_limit = item_limit_from_dict(inventory_dict['item_limit'])
    description = StaticResponse(f"{name}'s inventory")
    items = dict[str,Target]()
    if 'items' in inventory_dict:
        items = children_from_dict(name, inventory_dict['items'], item_factory, character_factory)
    return LocationDetail(name='inventory', description=description, children=items, item_limit=item_limit, hidden=True)

class NamedFactory[T:Named]:

    def __init__(self, constructor:Callable[[Any],T]):
        self.constructor = constructor
        self.objects = dict[T,T]()
        self.aliases = dict[str,T]()

    def get_all_named(self) -> list[T]:
        return list(self.objects.values())

    def many_from_dict(self, named_dict:list[dict[str,Any]]) -> list[T]:
        objects = list[T]()
        for object in named_dict:
            objects.append(self.one_from_dict(object))
        return objects
    
    def one_from_dict(self, named_dict:dict[str,Any]) -> T:
        name = named_dict['name']
        aliases = None
        if 'aliases' in named_dict:
            aliases = named_dict['aliases']
        return self.create_named(name, aliases)

    def create_named(self, name:str, aliases:Optional[list[str]]=None) -> T:
        new_object = self.constructor(name,aliases)
        if new_object in self.objects:
            return self.objects[new_object]
        for alias in new_object.get_aliases():
            if alias in self.aliases:
                print(f"Error: two objects {self.aliases[alias]} and {new_object} have the same alias. Only one will be created.")
                return self.aliases[alias]
        self.objects[new_object] = new_object
        for alias in new_object.get_aliases():
            self.aliases[alias] = new_object
        return new_object
    
    def get_named(self, alias:str) -> Optional[T]:
        return self.aliases.get(alias.lower(), None)

class StateFactory:

    def __init__(self):
        self.states = dict[State,State]()
        self.names  = dict[str,State]()

    def get_states(self) -> list[State]:
        return list(self.states.values())
    
    def create_state(self, name:str, actions_as_target:list[Action], actions_as_actor:list[Action], actions_as_tool:list[Action]) -> State:
        new_state = State.create_state(name,actions_as_target, actions_as_actor, actions_as_tool)
        if new_state in self.states:
            return self.states[new_state]
        name = new_state.get_name().lower()
        if name in self.names:
            print(f"Error: two States {self.names[name]} and {new_state} have the same name. Only one will be created.")
            return self.names[name]
        self.states[new_state] = new_state
        self.names[name] = new_state
        return new_state

    def get_state(self, name:str) -> Optional[State]:
        return self.names.get(name.lower(), None)
    
    def many_from_dict(self, state_dict:list[dict[str,Any]], action_factory:NamedFactory[Action]) -> list[State]:
        states = list[State]()
        for state in state_dict:
            name = state['name']
            actions_as_target = []
            if 'actions_as_target' in state:
                for action_name in state['actions_as_target']:
                    action = action_factory.get_named(action_name)
                    if action is None:
                        print(f"Can't find action {action_name} in {name}")
                    actions_as_target.append(action)
            actions_as_tool = []
            if 'actions_as_tool' in state:
                for action_name in state['actions_as_tool']:
                    action = action_factory.get_named(action_name)
                    if action is None:
                        print(f"Can't find action {action_name} in {name}")
                    actions_as_tool.append(action)
            actions_as_actor = []
            if 'actions_as_actor' in state:
                for action_name in state['actions_as_actor']:
                    action = action_factory.get_named(action_name)
                    if action is None:
                        print(f"Can't find action {action_name} in {name}")
                    actions_as_actor.append(action)
            states.append(self.create_state(name, actions_as_target, actions_as_actor, actions_as_tool))
        return states

class StateGroupFactory:

    def __init__(self):
        self.groups  = dict[StateGroup,StateGroup]()
        self.aliases = dict[str,StateGroup]()

    def create_state_group(self, name:str, states:list[State]) -> StateGroup:
        new_group = StateGroup(name, states)
        if new_group in self.groups:
            return self.groups[new_group]
        for alias in new_group.get_aliases():
            if alias in self.aliases:
                print(f"Error: two StateGroups {self.aliases[alias]} and {new_group} have the same name. Only one will be created.")
                return self.groups[alias]
        self.groups[new_group] = new_group
        for alias in new_group.get_aliases():
            self.aliases[alias] = new_group
        return new_group
    
    def get_state_group(self, alias:str) -> Optional[StateGroup]:
        return self.aliases.get(alias.lower(), None)
    
    def many_from_dict(self, group_dicts:list[dict[str,Any]], state_factory:StateFactory) -> list[StateGroup]:
        groups = []
        for group_dict in group_dicts:
            name = group_dict['name']
            states = list[State]()
            for state_name in group_dict['states']:
                state = state_factory.get_state(state_name)
                if state is None:
                    print(f"Can't find state {state_name} in {name}")
                states.append(state)
            groups.append(self.create_state_group(name, states))
        return groups

class StateGraphFactory:

    def __init__(self):
        self.graphs  = dict[StateGraph,StateGraph]()
        self.aliases = dict[str,StateGraph]()

    def get_state_graphs(self) -> list[StateGraph]:
        return list(self.graphs.values())

    def create_state_graph(self, name:str, current_state:StateGroup, target_graph:dict[StateGroup,dict[Action,StateGroup]]=None, tool_graph:dict[StateGroup,dict[Action,StateGroup]]=None, actor_graph:dict[StateGroup,dict[Action,StateGroup]]=None, time_graph:dict[StateGroup,tuple[int,StateGroup]]=None) -> StateGraph:
        new_graph = StateGraph(name, current_state, target_graph, tool_graph, actor_graph, time_graph)
        if new_graph in self.graphs:
            return self.graphs[new_graph]
        for alias in new_graph.get_aliases():
            if alias in self.aliases:
                print(f"Error: two StateGraphs {self.aliases[alias]} and {new_graph} have the same name. Only one will be created.")
                return self.graphs[alias]
        self.graphs[new_graph] = new_graph
        for alias in new_graph.get_aliases():
            self.aliases[alias] = new_graph
        return new_graph
    
    def get_state_graph(self, alias:str) -> Optional[StateGraph]:
        return self.aliases.get(alias.lower(), None).copy()
    
    def many_from_dict(self, graph_dicts:list[dict[str,Any]], state_factory:StateFactory, action_factory:NamedFactory[Action]) -> list[StateGraph]:
        graphs = list[StateGraph]()
        state_group_factory = StateGroupFactory()
        for graph_dict in graph_dicts:
            if 'state_groups' in graph_dict:
                state_group_factory = StateGroupFactory()
                state_group_factory.many_from_dict(graph_dict['state_groups'], state_factory)
                continue
            name = graph_dict['name']
            current_state = state_group_factory.get_state_group(graph_dict['current_state'])
            if current_state is None:
                print(f"Can't find state group {graph_dict['current_state']} in {name}")
            target_graph = dict[StateGroup,dict[Action,StateGroup]]()
            if 'target_graph' in graph_dict:
                for state_group1_name in graph_dict['target_graph']:
                    state_group1 = state_group_factory.get_state_group(state_group1_name)
                    if state_group1 is None:
                        print(f"Can't find state group {state_group1_name} in {name}")
                    target_graph[state_group1] = dict[Action,StateGroup]()
                    for action_name in graph_dict['target_graph'][state_group1_name]:
                        action = action_factory.get_named(action_name)
                        if action is None:
                            print(f"Can't find action {action_name} in {name}")
                        state_group2 = state_group_factory.get_state_group(graph_dict['target_graph'][state_group1_name][action_name])
                        if state_group2 is None:
                            print(f"Can't find state group {graph_dict['target_graph'][state_group1_name][action_name]} in {name}")
                        target_graph[state_group1][action] = state_group2
            tool_graph = dict[StateGroup,dict[Action,StateGroup]]()
            if 'tool_graph' in graph_dict:
                for state_group1_name in graph_dict['tool_graph']:
                    state_group1 = state_group_factory.get_state_group(state_group1_name)
                    if state_group1 is None:
                        print(f"Can't find state group {state_group1_name} in {name}")
                    tool_graph[state_group1] = dict[Action,StateGroup]()
                    for action_name in graph_dict['tool_graph'][state_group1_name]:
                        action = action_factory.get_named(action_name)
                        if action is None:
                            print(f"Can't find action {action_name} in {name}")
                        state_group2 = state_group_factory.get_state_group(graph_dict['tool_graph'][state_group1_name][action_name])
                        if state_group2 is None:
                            print(f"Can't find state group {graph_dict['tool_graph'][state_group1_name][action_name]} in {name}")
                        tool_graph[state_group1][action] = state_group2
            actor_graph = dict[StateGroup,dict[Action,StateGroup]]()
            if 'actor_graph' in graph_dict:
                for state_group1_name in graph_dict['actor_graph']:
                    state_group1 = state_group_factory.get_state_group(state_group1_name)
                    if state_group1 is None:
                        print(f"Can't find state group {state_group1_name} in {name}")
                    actor_graph[state_group1] = dict[Action,StateGroup]()
                    for action_name in graph_dict['actor_graph'][state_group1_name]:
                        action = action_factory.get_named(action_name)
                        if action is None:
                            print(f"Can't find action {action_name} in {name}")
                        state_group2 = state_group_factory.get_state_group(graph_dict['actor_graph'][state_group1_name][action_name])
                        if state_group2 is None:
                            print(f"Can't find state group {graph_dict['actor_graph'][state_group1_name][action_name]} in {name}")
                        actor_graph[state_group1][action] = state_group2
            time_graph = dict[StateGroup,tuple[int,StateGroup]]()
            if 'time_graph' in graph_dict:
                for state_group1_name in graph_dict['time_graph']:
                    state_group1 = state_group_factory.get_state_group(state_group1_name)
                    if state_group1 is None:
                        print(f"Can't find state group {state_group1_name} in {name}")
                    time,state_group2_name = graph_dict['time_graph'][state_group1_name]
                    state_group2 = state_group_factory.get_state_group(state_group2_name)
                    if state_group2 is None:
                        print(f"Can't find state group {state_group2_name} in {name}")
                    time_graph[state_group1] = (time, state_group2)
            graphs.append(self.create_state_graph(name, current_state, target_graph, tool_graph, actor_graph, time_graph))
        return graphs

class ItemFactory:

    def __init__(self):
        self.items = dict[Target,Target]()
        self.aliases = dict[str,Target]()

    def get_items(self) -> list[Target]:
        return list(self.items.values())

    def create_item(self, name:str, states:StateDisconnectedGraph, weight:float, value:float, size:float, aliases:list[str]=None) -> Target:
        new_item = Target(name, None, states, weight=weight, value=value, size=size, aliases=aliases)
        if new_item in self.items:
            return self.items[new_item]
        for alias in new_item.get_aliases():
            if alias in self.aliases:
                print(f"Error: two Items {self.aliases[alias]} and {new_item} have the same alias. Only one will be created.")
                return self.aliases[alias]
        self.items[new_item] = new_item
        for alias in new_item.get_aliases():
            self.aliases[alias] = new_item
        return new_item
    
    def get_item(self, alias:str) -> Optional[Target]:
        return self.aliases.get(alias.lower(), None)
    
    def many_from_dict(self, item_dicts:list[dict[str,Any]], action_factory:NamedFactory[Action], state_factory:StateFactory, state_graph_factory:StateGraphFactory) -> list[Target]:
        items = list[Target]()
        for item_dict in item_dicts:
            name = item_dict['name']
            aliases = item_dict.get('aliases', None)
            states = sdg_from_dict(name, item_dict['state'], state_factory, state_graph_factory, action_factory)
            weight = item_dict.get('weight', None)
            value  = item_dict.get('value', None)
            size   = item_dict.get('size', None)
            items.append(self.create_item(name, states, weight, value, size, aliases))
        return items
    
    def update(self, item_dicts:list[dict[str,Any]], character_factory:'CharacterFactory', detail_factory:'LocationDetailFactory', location_factory:'LocationFactory', state_factory:StateFactory, action_factory:NamedFactory[Action], achievement_factory:NamedFactory[Achievement]) -> None:
        for item_dict in item_dicts:
            name = item_dict['name']
            item = self.get_item(name)
            item.description = response_from_input(name, item_dict['description'], self, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
            if item is None:
                print(f"Can't find item {name} in items")
            if 'item_response' in item_dict:
                item.item_responses = item_responses_from_dict(name, item_dict['item_response'], self, character_factory)
            if 'details' in item_dict:
                new_details = detail_factory.many_from_dict(item_dict['details'])
                detail_factory.update(item_dict['details'], self, character_factory, state_factory, achievement_factory, location_factory, action_factory)
                children = {detail_factory.get_detail(detail.get_name()).get_name():detail_factory.get_detail(detail.get_name()) for detail in new_details}
                item._set_children(children)
                for detail in new_details:
                    detail_factory.remove_detail(detail.get_name())
            if 'visible_requirements' in item_dict:
                item.visible_requirements = requirements_from_dict(name, item_dict['visible_requirements'], self, character_factory, state_factory, achievement_factory, location_factory, detail_factory)
            if 'target_responses' in item_dict:
                item.target_responses = action_responses_from_dict(name, item_dict['target_responses'], self, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
            if 'tool_responses' in item_dict:
                item.tool_responses   = action_responses_from_dict(name, item_dict['tool_responses'],   self, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
            if 'state_responses' in item_dict:
                item.state_responses  = state_responses_from_dict(name,  item_dict['state_responses'],  self, character_factory, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
            
class SkillSetFactory:

    def __init__(self):
        self.skill_sets = dict[SkillSet,SkillSet]()
        self.aliases = dict[str,SkillSet]()

    def create_skill_set(self, name:str, skills:dict[Skill,int], default_proficiency:int=None) -> SkillSet:
        if default_proficiency is None:
            new_skill_set = SkillSet(name, skills)
        else:
            new_skill_set = SkillSet(name, skills, default_proficiency)
        if new_skill_set in self.skill_sets:
            return self.skill_sets[new_skill_set]
        for alias in new_skill_set.get_aliases():
            if alias in self.aliases:
                print(f"Error: two SkillSets {self.aliases[alias]} and {new_skill_set} have the same alias. Only one will be created.")
                return self.aliases[alias]
        self.skill_sets[new_skill_set] = new_skill_set
        for alias in new_skill_set.get_aliases():
            self.aliases[alias] = new_skill_set
        return new_skill_set
    
    def get_skill_set(self, alias:str) -> Optional[SkillSet]:
        return self.aliases.get(alias.lower(), None)
    
    def many_from_dict(self, skill_set_dict:list[dict[str,Any]], skill_factory:NamedFactory[Skill]) -> list[SkillSet]:
        skill_sets = list[SkillSet]()
        for skill_set in skill_set_dict:
            name = skill_set['name']
            skills = dict[Skill,int]()
            if 'skills' in skill_set:
                for skill_name in skill_set['skills']:
                    skill = skill_factory.get_named(skill_name)
                    if skill is None:
                        print(f"Can't find skill {skill_name} in {name}")
                    skills[skill] = skill_set['skills'][skill_name]
            proficiency = None
            if 'default_proficiency' in skill_set:
                proficiency = skill_set['default_proficiency']
            skill_sets.append(self.create_skill_set(name, skills, proficiency))
        return skill_sets

class CharacterFactory:

    def __init__(self):
        self.characters = dict[Actor,Actor]()
        self.aliases = dict[str,Actor]()

    def get_characters(self) -> list[Actor]:
        return list(self.characters.values())

    def create_character(self, 
                         name:str, 
                         type:str, 
                         states:StateDisconnectedGraph, 
                         skills:SkillSet,
                         weight:float,
                         size:float,
                         value:float,
                         achievements:list[Achievement],
                         aliases:list[str]) -> Actor:
        new_character = Actor(name, None, type, states, skills, weight=weight, size=size, value=value, achievements=achievements, aliases=aliases)
        if new_character in self.characters:
            return self.characters[new_character]
        for alias in new_character.get_aliases():
            if alias in self.aliases:
                print(f"Error: two Characters {self.aliases[alias]} and {new_character} have the same alias. Only one will be created.")
                return self.aliases[alias]
        self.characters[new_character] = new_character
        for alias in new_character.get_aliases():
            self.aliases[alias] = new_character
        return new_character
    
    def get_character(self, alias:str) -> Optional[Actor]:
        return self.aliases.get(alias.lower(), None)
    
    def many_from_dict(self, 
                       character_dicts:list[dict[str,Any]],
                       skills_factory:SkillSetFactory,
                       action_factory:NamedFactory[Action],
                       state_factory:StateFactory,
                       achievement_factory:NamedFactory[Achievement],
                       state_graph_factory:StateGraphFactory) -> Actor:
        characters = list[Actor]()
        for character_dict in character_dicts:
            name = character_dict['name']
            type = character_dict['type']
            states = sdg_from_dict(name, character_dict['state'], state_factory, state_graph_factory, action_factory)
            if states is None:
                print(f"Can't find sdg {character_dict["states"]} in {name}")
            skills = skills_factory.get_skill_set(character_dict['skills'])
            if skills is None:
                print(f"Can't find SkillSet {character_dict['skills']} in {name}")
            weight = character_dict.get('weight', None)
            size   = character_dict.get('size',   None)
            value  = character_dict.get('value',  None)
            achievements = list[Achievement]()
            if 'achievements' in character_dict:
                for achievement_name in character_dict['achievements']:
                    achievement = achievement_factory.get_named(achievement_name)
                    if achievement is None:
                        print(f"Can't find achievement {achievement_name} in {name}")
                    achievements.append(achievement)
            aliases = character_dict.get('aliases', None)
            characters.append(self.create_character(name, type, states, skills, weight, size, value, achievements, aliases))
        return characters
    
    def update(self, character_dicts:list[dict[str,Any]], item_factory:'ItemFactory', detail_factory:'LocationDetailFactory', location_factory:'LocationFactory', state_factory:StateFactory, action_factory:NamedFactory[Action], achievement_factory:NamedFactory[Achievement]) -> None:
        for character_dict in character_dicts:
            name = character_dict['name']
            character = self.get_character(name)
            character.description = response_from_input(name, character_dict['description'], item_factory, self, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
            if character is None:
                print(f"Can't find character {name} in characters")
            if 'item_response' in character_dict:
                character.item_responses = item_responses_from_dict(name, character_dict['item_response'], item_factory, self)
            if 'details' in character_dict:
                new_details = detail_factory.many_from_dict(character_dict['details'])
                detail_factory.update(character_dict['details'], item_factory, self, state_factory, achievement_factory, location_factory)
                children = {detail_factory.get_detail(detail.get_name()).get_name():detail_factory.get_detail(detail.get_name()) for detail in new_details}
                character._set_children(children)
                for detail in new_details:
                    detail_factory.remove_detail(detail.get_name())
            if 'inventory' in character_dict:
                inventory = inventory_from_dict(name, character_dict['inventory'], item_factory, self)
                inventory.parent = character
                character.children['inventory'] = inventory
            if 'visible_requirements' in character_dict:
                character.visible_requirements = requirements_from_dict(name, character_dict['visible_requirements'], item_factory, self, state_factory, achievement_factory, location_factory, detail_factory)
            if 'actor_responses' in character_dict:
                character.actor_responses = action_responses_from_dict(name, character_dict['actor_responses'],   item_factory, self, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
            if 'target_responses' in character_dict:
                character.target_responses = action_responses_from_dict(name, character_dict['target_responses'], item_factory, self, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
            if 'tool_responses' in character_dict:
                character.tool_responses   = action_responses_from_dict(name, character_dict['tool_responses'],   item_factory, self, detail_factory, location_factory, state_factory, action_factory, achievement_factory)
            if 'state_responses' in character_dict:
                character.state_responses  = state_responses_from_dict(name,  character_dict['state_responses'],  item_factory, self, detail_factory, location_factory, state_factory, action_factory, achievement_factory)

class LocationDetailFactory:

    def __init__(self):
        self.details = dict[LocationDetail,LocationDetail]()
        self.aliases = dict[str,LocationDetail]()

    def get_details(self) -> list[LocationDetail]:
        return list(self.details.values())

    def create_detail(self, name:str="default", *, hidden:bool=False, item_limit:ItemLimit=None, aliases:list[str]=None) -> SkillSet:
        new_detail = LocationDetail(name=name, description=None, hidden=hidden, item_limit=item_limit, aliases=aliases)
        if new_detail in self.details:
            return self.details[new_detail]
        for alias in new_detail.get_aliases():
            if alias in self.aliases:
                print(f"Error: two LocationDetails {self.aliases[alias]} and {new_detail} have the same alias. Only one will be created.")
                return self.aliases[alias]
        self.details[new_detail] = new_detail
        for alias in new_detail.get_aliases():
            self.aliases[alias] = new_detail
        return new_detail
    
    def get_detail(self, alias:str) -> Optional[LocationDetail]:
        return self.aliases.get(alias.lower(), None)
    
    def remove_detail(self, alias:str) -> None:
        detail = self.get_detail(alias)
        del self.details[detail]
        for alias2 in detail.get_aliases():
            del self.aliases[alias2]
    
    def one_from_dict(self, detail_dict:dict[str,Any]) -> LocationDetail:
        name = detail_dict['name']
        hidden  = detail_dict.get('hidden', False)
        aliases = detail_dict.get('aliases', None)
        item_limit = item_limit_from_dict(detail_dict['item_limit']) if 'item_limit' in detail_dict else None
        return self.create_detail(name, hidden=hidden, item_limit=item_limit, aliases=aliases)
    
    def many_from_dict(self, detail_dicts:list[dict[str,Any]]) -> list[LocationDetail]:
        details = list[LocationDetail]()
        for detail_dict in detail_dicts:
            details.append(self.one_from_dict(detail_dict))
        return details
    
    def update(self, detail_dicts:list[dict[str,Any]], item_factory:ItemFactory, character_factory:CharacterFactory, state_factory:StateFactory, achievement_factory:NamedFactory[Achievement], location_factory:'LocationFactory', action_factory:'NamedFactory[Action]') -> None:
        for detail_dict in detail_dicts:
            name = detail_dict['name']
            detail = self.get_detail(name)
            if 'description' in detail_dict:
                detail.description = response_from_input(name, detail_dict['description'], item_factory, character_factory, self, location_factory, state_factory, action_factory, achievement_factory)
            if detail is None:
                print(f"Can't find detail {detail_dict["name"]} in self")
            if 'item_response' in detail_dict:
                detail.item_responses = item_responses_from_dict(name, detail_dict, item_factory, character_factory, self, location_factory, state_factory, action_factory, achievement_factory)
            if 'contents' in detail_dict:
                detail._set_children(children_from_dict(name, detail_dict['contents'], item_factory, character_factory, self))
            if 'visible_requirements' in detail_dict:
                detail.visible_requirements = requirements_from_dict(name, detail_dict['visible_requirements'], item_factory, character_factory, state_factory, achievement_factory, location_factory, self) 

class LocationFactory:

    def __init__(self):
        self.locations = dict[SkillSet,SkillSet]()
        self.aliases = dict[str,SkillSet]()

    def get_locations(self) -> list[Location]:
        return list(self.locations.values())

    def create_location(self,
                        name:str, 
                        description:ResponseString,
                        paths:dict[Direction,Path], *, 
                        direction_responses:dict[Direction,str]=None,
                        contents:dict[str,HasLocation]=None,
                        start_location:bool=False,
                        item_limit:ItemLimit=None,
                        visible_requirements:list[ActionRequirement]=None,
                        item_responses:list[HasLocation,str]=None,
                        aliases:list[str]=None) -> Location:
        new_location = Location(name, description, paths, direction_responses=direction_responses, start_location=start_location, children=contents, item_limit=item_limit, visible_requirements=visible_requirements, item_responses=item_responses, aliases=aliases)
        if new_location in self.locations:
            return self.locations[new_location]
        for alias in new_location.get_aliases():
            if alias in self.aliases:
                print(f"Error: two Locations {self.aliases[alias]} and {new_location} have the same alias. Only one will be created.")
                return self.aliases[alias]
        self.locations[new_location] = new_location
        for alias in new_location.get_aliases():
            self.aliases[alias] = new_location
        return new_location
    
    def get_location(self, alias:str) -> Optional[Location]:
        return self.aliases.get(alias.lower(), None)

    def many_from_dict(self, location_dicts:list[dict[str,Any]], character_factory:CharacterFactory, item_factory:ItemFactory, direction_factory:NamedFactory[Direction], state_factory:StateFactory, achievement_factory:NamedFactory[Achievement], action_factory:NamedFactory[Action]) -> tuple[list[Location],LocationDetailFactory]:
        locations = list[Location]()
        detail_factory = LocationDetailFactory()
        for location_dict in location_dicts:
            name = location_dict['name']
            aliases = location_dict.get('aliases', None)
            paths = dict[Direction,Path]()
            if 'paths' in location_dict:
                for direction_name, path_dict in location_dict['paths'].items():
                    direction = direction_factory.get_named(direction_name)
                    if direction is None:
                        print(f"Can't find direction {direction_name} in {name}")
                    try:
                        path = path_from_dict(path_dict, item_factory, character_factory, state_factory, achievement_factory)
                    except TypeError as e:
                        print(e)
                        print(f"Path error in {name}")
                    paths[direction] = path
            direction_responses = direction_responses_from_dict(name, location_dict['direction_responses'], direction_factory, item_factory, character_factory, detail_factory, self, state_factory, action_factory, achievement_factory) if 'direction_responses' in location_dict else None
            details = []
            if 'details' in location_dict:
                details = detail_factory.many_from_dict(location_dict['details'])
            contents = {detail.get_name():detail for detail in details}
            if 'contents' in location_dict:
                for child_name in location_dict['contents']:
                    child = character_factory.get_character(child_name)
                    if child is None:
                        child = item_factory.get_item(child_name)
                    if child is None:
                        child = detail_factory.get_detail(child_name)
                    if child is None:
                        print(f"Can't find child {child_name} in {name}")
                    contents[child.get_name()] = child
            start_location = False
            if 'start' in location_dict:
                start_location = location_dict['start']
            
            item_limit = item_limit_from_dict(location_dict['item_limit']) if 'item_limit' in location_dict else None
            visible_requirements = requirements_from_dict(name, location_dict['visible_requirements'], item_factory, character_factory, state_factory, achievement_factory) if 'visible_requirements' in location_dict else None
            item_responses = item_responses_from_dict(name, location_dict['item_responses'], item_factory, character_factory, detail_factory, self, state_factory, action_factory, achievement_factory) if 'item_responses' in location_dict else None
            description = response_from_input(name, location_dict['description'], item_factory, character_factory, detail_factory, self, state_factory, action_factory, achievement_factory)
            
            locations.append(self.create_location(name, description, paths, direction_responses=direction_responses, contents=contents, start_location=start_location, item_limit=item_limit, visible_requirements=visible_requirements, item_responses=item_responses, aliases=aliases))
            
        # for each path set the end to the correct location
        # (this can't be done earlier because the end location might not exist yet)
        for location_dict in location_dicts:
            location = self.get_location(location_dict['name'])
            if location is None:
                print(f"Can't find location {location_dict['name']} at end")
            if 'paths' in location_dict:
                for direction_name,path_dict in location_dict['paths'].items():
                    direction = direction_factory.get_named(direction_name)
                    if direction is None:
                        print(f"Can't find direction {direction_name} in {location_dict['name']}")
                    if location._get_path(direction)[0]._set_end(self, detail_factory) is not None:
                        print(f"bad end in {location.name}")

                    location.paths[direction].description = response_from_input(name, path_dict['description'], item_factory, character_factory, detail_factory, self, state_factory, action_factory, achievement_factory)
                    if 'visible_requirements' in path_dict:
                        location.paths[direction].visible_requirements = requirements_from_dict(name, path_dict['visible_requirements'], item_factory, character_factory, state_factory, achievement_factory, self, detail_factory)
                    if 'passing_requirements' in path_dict:
                        location.paths[direction].passing_requirements = requirements_from_dict(name, path_dict['passing_requirements'], item_factory=item_factory, character_factory=character_factory, state_factory=state_factory, achievement_factory=achievement_factory, location_factory=self, detail_factory=detail_factory)
                    if 'path_items' in path_dict:
                        location.paths[direction]._set_children(children_from_dict(name, path_dict['path_items'], item_factory, character_factory, detail_factory))
                    if 'item_responses' in path_dict:
                        location.paths[direction].item_responses = item_responses_from_dict(name, path_dict['item_responses'], item_factory, character_factory, detail_factory, self, state_factory, action_factory, achievement_factory)
        
            # this can only be done once all details, characters, and items are in
            if 'details' in location_dict:
                detail_factory.update(location_dict['details'], item_factory, character_factory, state_factory, achievement_factory, self, action_factory)
        return locations, detail_factory

class CharacterControlFactory:

    def __init__(self):
        self.characters = dict[Actor,CharacterController]()

    def create_character(self, character:Actor, controller:CharacterController) -> None:
        self.characters[character] = controller
    
    def get_controller(self, character:Actor) -> Optional[CharacterController]:
        return self.characters.get(character, None)
    
    def many_from_dict(self, controller_dicts:list[dict[str,Any]], character_factory:CharacterFactory) -> None:
        for controller_dict in controller_dicts:
            character = character_factory.get_character(controller_dict['character'])
            if character is None:
                print(f"Can't find character {controller_dict['character']} in controller")
            controller = NPCController()
            if 'controller' in controller_dict:
                controller_type = controller_dict['controller']
                if controller_type.lower() == 'user':
                    controller = CommandLineController()
                else:
                    controller = NPCController()
            self.create_character(character, controller)
    
    def playable_characters(self) -> int:
        return len([1 for _,control in self.characters.items() if isinstance(control, CommandLineController)])
