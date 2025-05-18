from typing import Optional, Any

from utils.relator      import NameFinder
from models.named       import Action, Direction
from models.actors      import ItemLimit, HasLocation, Location, Path, Target, Actor, LocationDetail, SingleEndPath, MultiEndPath, Achievement
from models.requirement import ActionRequirement, CharacterAchievementRequirement, CharacterStateRequirement, ItemsHeldRequirement, ItemStateRequirement, ItemPlacementRequirement
from models.state       import State, StateGroup, StateGraph, Skill, StateDisconnectedGraph
from models.response    import ResponseString, StaticResponse, CombinationResponse, ItemStateResponse, ContentsResponse, RandomResponse, ContentsWithStateResponse
from controls.character_control import CharacterController, CommandLineController, NPCController

# REQUIREMENTS

def character_state_requirements_from_dict(name:str, requirement_dict:dict[str,Any], name_space:NameFinder) -> CharacterStateRequirement:
    states_needed = dict[State,tuple[bool,ResponseString]]()
    for state_id, needed in requirement_dict.items():
        state = name_space.get_from_id(state_id, 'state')
        if isinstance(needed, bool):
            states_needed[state] = (needed, None)
        else:
            states_needed[state] = (needed[0], response_from_input(name, needed[1], name_space))
    return CharacterStateRequirement(states_needed)

def character_achievement_requirements_from_dict(name:str, requirement_dict:dict[str,Any], name_space:NameFinder) -> CharacterAchievementRequirement:
    achievements_needed = dict[Achievement,tuple[bool,ResponseString]]()
    for achievement_id, needed in requirement_dict.items():
        achievement = name_space.get_from_id(achievement_id, 'achievement')
        if isinstance(needed, bool):
            achievements_needed[achievement] = (needed,None)
        else:
            achievements_needed[achievement] = (needed[0], response_from_input(name, needed[1], name_space))
    return CharacterAchievementRequirement(achievements_needed)

def item_state_requirements_from_dict(name:str, requirement_dict:dict[str,Any], name_space:NameFinder) -> ItemStateRequirement:
    item_states = dict[Target,dict[State,tuple[bool,ResponseString]]]()
    for item_id, states_needed_raw in requirement_dict.items():
        item = name_space.get_from_id(item_id, ['target','actor'])
        states_needed = dict[State,tuple[bool,str]]()
        for state_id, needed in states_needed_raw.items():
            state = name_space.get_from_id(state_id, 'state')
            if isinstance(needed, bool):
                states_needed[state] = (needed,None)
            else:
                states_needed[state] = (needed[0], response_from_input(name, needed[1], name_space))
        item_states[item] = states_needed
    return ItemStateRequirement(item_states)

def item_placement_requirements_from_dict(name:str, requirement_dict:dict[str,Any], name_space:NameFinder) -> ItemPlacementRequirement:
    item_placements = dict[Target,list[tuple[Location,bool,ResponseString]]]()
    for item_id, location_info in requirement_dict.items():
        item = name_space.get_from_id(item_id, ['target','actor'])
        placements = list[tuple[Location,bool,ResponseString]]()
        for location_id, needed, response in location_info:
            location = name_space.get_from_id(location_id, ['location', 'locationdetail'])
            placements.append((location, needed, response_from_input(name, response, name_space)))
        item_placements[item] = placements
    return ItemPlacementRequirement(item_placements)

def items_held_requirement_from_dict(name:str, requirement_dict:dict[str,Any], name_space:NameFinder) -> ItemsHeldRequirement:
    items_needed = dict[Target,tuple[bool,ResponseString]]()
    for item_id, needed in requirement_dict.items():
        item = name_space.get_from_id(item_id, ['target', 'actor'])
        if isinstance(needed, bool):
            items_needed[item] = (needed,None)
        else:
            items_needed[item] = (needed[0], response_from_input(name, needed[1], name_space))
    return ItemsHeldRequirement(items_needed)

def requirements_from_dict(name:str, requirements_dict:dict[str,Any], name_space:NameFinder, setup_space:NameFinder) -> list[ActionRequirement]:
    requirements = list[ActionRequirement]()
    if 'character_state_requirements' in requirements_dict:
        states_needed_raw = requirements_dict['character_state_requirements']
        requirements.append(character_state_requirements_from_dict(name, states_needed_raw, name_space))
    if 'character_achievement_requirements' in requirements_dict:
        achievements_needed_raw = requirements_dict['character_achievement_requirements']
        requirements.append(character_achievement_requirements_from_dict(name, achievements_needed_raw, name_space))
    if 'item_state_requirements' in requirements_dict:
        item_states_raw = requirements_dict['item_state_requirements']
        requirements.append(item_state_requirements_from_dict(name, item_states_raw, name_space))
    if 'items_held_requirements' in requirements_dict:
        items_needed_raw = requirements_dict['items_held_requirements']
        requirements.append(items_held_requirement_from_dict(name, items_needed_raw, name_space))
    if 'item_placement_requirements' in requirements_dict:
        item_placements_raw = requirements_dict['item_placement_requirements']
        requirements.append(item_placement_requirements_from_dict(name, item_placements_raw, name_space))
    return requirements

# RESPONSES

def contents_response_from_dict(name:str, response_dict:dict[str,str], name_space:NameFinder) -> ContentsResponse:
    target_id = response_dict['target'] if 'target' in response_dict else name
    target = name_space.get_from_id(target_id, ['target', 'actor', 'locationdetail'])
    full_response  = response_from_input(name, response_dict['full'], name_space)
    empty_response = response_from_input(name, response_dict['empty'], name_space)
    return ContentsResponse(full_response, empty_response, target)

def contents_with_state_response_from_dict(name:str, response_dict:dict[str,str|dict[str,str]], name_space:NameFinder) -> ItemStateResponse:
    target_id = response_dict['target'] if 'target' in response_dict else name
    target = name_space.get_from_id(target_id, ['target', 'actor'])
    responses = dict[State,str]()
    for state_id, response in response_dict['responses'].items():
        state = name_space.get_from_id(state_id, 'state')
        responses[state] = response_from_input(name, response, name_space)
    default = response_dict.get('default', None)
    return ContentsWithStateResponse(target, responses, default=default)

def item_state_response_from_dict(name:str, response_dict:dict[str,str|dict[str,str]], name_space:NameFinder) -> ItemStateResponse:
    target_id = response_dict['target'] if 'target' in response_dict else name
    target = name_space.get_from_id(target_id, ['target', 'actor'])
    responses = dict[State,str]()
    for state_id, response in response_dict['responses'].items():
        state = name_space.get_from_id(state_id)
        responses[state] = response_from_input(name, response, name_space)
    default = response_from_input(name, response_dict.get('default', None), name_space)
    return ItemStateResponse(target, responses, default=default)

def random_response_from_list(name, response_list:list[str|dict], name_space:NameFinder) -> RandomResponse:
    responses = list[ResponseString]()
    for response in response_list:
        responses.append(response_from_input(name, response, name_space))
    return RandomResponse(responses)

def response_from_list(name:str, input_list:list[str|dict[str,Any]], name_space:NameFinder) -> CombinationResponse:
    responses = list[ResponseString]()
    for response in input_list:
        responses.append(response_from_input(name, response, name_space))
    return CombinationResponse(responses)

def response_from_dict(name:str, response_dict:dict[str,Any], name_space:NameFinder) -> ResponseString:
    match response_dict['type']:
        case 'item_state':
            return item_state_response_from_dict(name, response_dict, name_space)
        case 'contents':
            return contents_response_from_dict(name, response_dict, name_space)
        case 'contents_with_state':
            return item_state_response_from_dict(name, response_dict, name_space)
        case 'random':
            return random_response_from_list(name, response_dict['responses'], name_space)
        case _:
            print(f'In {name} unknown response type {response_dict['type']}')

def response_from_input(name:str, input:str|dict[str,Any]|list, name_space:NameFinder) -> ResponseString:
    response = None
    if isinstance(input, str):
        response = StaticResponse(input)
    elif isinstance(input, list):
        response = response_from_list(name, input, name_space)
    elif isinstance(input, dict):
        response = response_from_dict(name, input, name_space)
    elif input is None:
        return None
    else:
        print(f"Unexpected type for response: {type(input)}")
    if response is None:
        print(f"None response in {name}")
    return response

# OTHER RESPONSES

def item_responses_from_dict(name:str, response_dict:dict[str,Any], name_space:NameFinder) -> dict['HasLocation',str]:
    responses = dict[HasLocation,ResponseString]()
    for item_id, response in response_dict:
        item = name_space.get_from_id(item_id, ['target', 'actor'])
        responses[item] = response_from_input(name, response, name_space)
    return responses

def action_responses_from_dict(name:str, response_dict:dict[str,Any], name_space:NameFinder) -> dict[Action,str]:
    responses = dict[Action,ResponseString]()
    for action_id, response in response_dict.items():
        action = name_space.get_from_id(action_id, 'action')
        responses[action] = response_from_input(name, response, name_space)
    return responses

def state_responses_from_dict(name:str, response_dict:dict[str,Any], name_space:NameFinder) -> dict[State,str]:
    responses = dict[State,ResponseString]()
    for state_id, response in response_dict.items():
        state = name_space.get_from_id(state_id, 'state')
        responses[state] = response_from_input(name, response, name_space)
    return responses

def direction_responses_from_dict(name:str, response_dict:dict[str,Any], name_space:NameFinder) -> dict[Direction,str]:
    responses = dict[Direction,ResponseString]()
    for direction_id, response in response_dict.items():
        direction = name_space.get_from_id(direction_id, 'direction')
        responses[direction] = response_from_input(name, response, name_space)
    return responses

# OTHER HELPERS

def children_from_dict(name, children_dict:dict[str,Any], name_space:NameFinder) -> list[HasLocation]:
    children = list[HasLocation]()
    for item_id in children_dict:
        item = name_space.get_from_id(item_id, ['target', 'actor', 'locationdetail'])
        children.append(item)
    return children

def item_limit_from_dict(limit_dict:dict[str,Any]) -> ItemLimit:
    size   = limit_dict.get('size',   None)
    weight = limit_dict.get('weight', None)
    value  = limit_dict.get('value',  None)
    return ItemLimit(size_limit=size, weight_limit=weight, value_limit=value)

# NAMED

def one_from_dict_named(named_dict:dict[str,Any], *, name:str=None) -> dict[str,Any]:
    inputs            = dict[str,Any]()
    inputs['name']    = named_dict['name'] if name is None else name
    inputs['id']      = named_dict.get('id', None)
    inputs['aliases'] = named_dict.get('aliases', None)
    return inputs

def many_from_dict_named(named_dicts:list[dict[str,Any]]) -> list[dict[str,Any]]:
    return [one_from_dict_named(named_dict) for named_dict in named_dicts]

# STATE

def input_list(ids:list[str], name_space:NameFinder, category:str=None) -> list:
    items = list()
    for id in ids:
        item = name_space.get_from_id(id, category)
        items.append(item)
    return items

def one_from_dict_state(state_dict:dict[str,Any], name_space:NameFinder) -> dict[str,Any]:
    inputs = one_from_dict_named(state_dict)
    try:
        inputs['actions_as_target'] = input_list(state_dict['actions_as_target'], name_space, 'action') if 'actions_as_target' in state_dict else []
        inputs['actions_as_tool']   = input_list(state_dict['actions_as_tool'],   name_space, 'action') if 'actions_as_tool'   in state_dict else []
        inputs['actions_as_actor']  = input_list(state_dict['actions_as_actor'],  name_space, 'action') if 'actions_as_actor'  in state_dict else []
    except ValueError as e:
        print(f"Error in state {inputs['name']}: {e}")
    return inputs

def many_from_dict_state(state_dicts:dict[str,Any], name_space:NameFinder) -> list[dict[str,Any]]:
    return [one_from_dict_state(state_dict, name_space) for state_dict in state_dicts]

# STATE GROUP

def one_from_dict_state_group(sg_dict:dict[str,Any], name_space:NameFinder) -> dict[str,Any]:
    inputs = one_from_dict_named(sg_dict)
    try:
        inputs['states'] = input_list(sg_dict['states'], name_space, 'state') if 'states' in sg_dict else []
    except ValueError as e:
        print(f"Error in state group {inputs['name']}: {e}")
    return inputs

def many_from_dict_state_group(sg_dicts:dict[str,Any], name_space:NameFinder) -> list[dict[str,Any]]:
    return [one_from_dict_state_group(sg_dict, name_space) for sg_dict in sg_dicts]

# STATE GRAPH

def input_state_graph(graph_dict:dict[str,dict[str,str]], name_space:NameFinder, setup_space:NameFinder) -> dict[StateGroup,dict[Action,StateGroup]]:
    graph = dict[StateGroup,dict[Action,StateGroup]]()
    for state_group1_id, action_graph in graph_dict.items():
        state_group1 = setup_space.get_from_id(state_group1_id, 'stategroup')
        graph[state_group1] = dict[Action,StateGroup]()
        for action_id, state_group2_id in action_graph.items():
            action = name_space.get_from_id(action_id, 'action')
            state_group2 = setup_space.get_from_id(state_group2_id, 'stategroup')
            graph[state_group1][action] = state_group2
    return graph

def input_time_graph(graph_dict:dict[str,dict[str,str]], name_space:NameFinder, setup_space:NameFinder) -> dict[StateGroup,tuple[int,StateGroup]]:
    graph = dict[StateGroup,tuple[int,StateGroup]]()
    for state_group1_id, time_info in graph_dict:
        state_group1 = setup_space.get_from_id(state_group1_id, 'stategroup')
        time,state_group2_id = time_info
        state_group2 = setup_space.get_from_id(state_group2_id, 'stategroup')
        graph[state_group1] = (time, state_group2)
    return graph

# Note: only copies of these should be used
def one_from_dict_state_graph(sg_dict:dict[str,Any], name_space:NameFinder, setup_space:NameFinder) -> dict[str,Any]:
    inputs = one_from_dict_named(sg_dict)
    try:
        inputs['current_state'] = setup_space.get_from_id(sg_dict['current_state'], 'stategroup')
        inputs['target_graph']  = input_state_graph(sg_dict['target_graph'], name_space, setup_space) if 'target_graph' in sg_dict else dict[StateGroup,dict[Action,StateGroup]]()
        inputs['tool_graph']    = input_state_graph(sg_dict['tool_graph'],   name_space, setup_space) if 'tool_graph'   in sg_dict else dict[StateGroup,dict[Action,StateGroup]]()
        inputs['actor_graph']   = input_state_graph(sg_dict['actor_graph'],  name_space, setup_space) if 'actor_graph'  in sg_dict else dict[StateGroup,dict[Action,StateGroup]]()
    except ValueError as e:
        print(f"Error in state graph {inputs['name']}: {e}")
    return inputs

def many_from_dict_state_graph(sg_dicts:list[dict[str,Any]], name_space:NameFinder, setup_space:NameFinder) -> list[dict[str,Any]]:
    return [one_from_dict_state_graph(sg_dict, name_space, setup_space) for sg_dict in sg_dicts]

# SDG

def one_from_dict_sdg(name:str, sdg_dict:dict[str,list[str]], name_space:NameFinder, setup_space:NameFinder) -> dict[str,Any]:
    inputs = one_from_dict_named(sdg_dict, name=f"{name} state")
    state_graphs = list[StateGraph]()
    try:
        if "states" in sdg_dict:
            for state_id in sdg_dict["states"]:
                state = name_space.get_from_id(state_id, 'state')
                state_group = StateGroup(state.get_name(), [state])
                state_graphs.append(StateGraph(state_group.get_name(), state_group))
        if "breakable" in sdg_dict:
            breakable_states = list[State]()
            for state_id in sdg_dict["breakable"]:
                state = name_space.get_from_id(state_id)
            state_group = StateGroup(f"{name}_breakable", breakable_states)
            break_action = name_space.get_from_name("break", 'action')[0]
            broken_state = name_space.get_from_name("broken", 'state')[0]
            broken_group = StateGroup("broken", [broken_state])
            target_graph = {state_group: {break_action: broken_group}}
            state_graphs.append(StateGraph(f"{name}_breakable", state_group, target_graph=target_graph))
        if "graphs" in sdg_dict:
            for graph_id in sdg_dict["graphs"]:
                graph = setup_space.get_from_id(graph_id, 'stategraph').copy()
                state_graphs.append(graph)
        inputs['state_graphs'] = state_graphs
    except ValueError as e:
        print(f"Error in sdg {inputs['name']}: {e}")
    return inputs

def one_from_dict_inventory(name:str, inventory_dict:dict[str,Any], name_space:NameFinder) -> dict[str,Any]:
    item_limit = item_limit_from_dict(inventory_dict['item_limit']) if 'item_limit' in inventory_dict else None
    description = StaticResponse(f"{name}'s inventory")
    items = dict[str,Target]()
    if 'items' in inventory_dict:
        items = children_from_dict(name, inventory_dict['items'], name_space)
    return {
        'name'        : 'inventory',
        'description' : description,
        'children'    : items,
        'item_limit'  : item_limit,
        'hidden'      : True,
        'id'          : f"{name}'s inventory"
    }

# ITEMS

def one_from_dict_item(item_dict:dict[str,Any], name_space:NameFinder, setup_space:NameFinder) -> dict[str,Any]:
    inputs = one_from_dict_named(item_dict)
    try:
        sdg_inputs       = one_from_dict_sdg(inputs['name'], item_dict['state'], name_space, setup_space)
        sdg              = StateDisconnectedGraph(**sdg_inputs)
        inputs['states'] = sdg
        inputs['weight'] = item_dict.get('weight', None)
        inputs['value']  = item_dict.get('value',  None)
        inputs['size']   = item_dict.get('size',   None)
        inputs['description'] = None
    except ValueError as e:
        print(f"Error in item {inputs['name']}: {e}")
    return inputs

def many_from_dict_item(item_dicts:list[dict[str,Any]], name_space:NameFinder, setup_space:NameFinder) -> list[dict[str,Any]]:
    return [one_from_dict_item(item_dict, name_space, setup_space) for item_dict in item_dicts]

def update_item(item_dict:dict[str,Any], name_space:NameFinder, setup_space:NameFinder) -> None:
    name = item_dict['name']
    id   = item_dict['id'] if 'id' in item_dict else name
    id   = id.lower()
    item = name_space.get_from_id(id)
    assert isinstance(item, Target)
    try:
        item.description = response_from_input(name, item_dict['description'], name_space)
        if 'details' in item_dict:
            new_detail_inputs = many_from_dict_detail(item_dict['details'], parent_id=name)
            new_details = [LocationDetail(**kwargs) for kwargs in new_detail_inputs]
            success = name_space.add_many(new_details)
            fails = [kwargs['name'] for s,kwargs in zip(success,new_detail_inputs) if not s]
            if len(fails) > 0: print(f"In {name} failed to add: {fails}")
            assert all(success)
            item._set_children(new_details)
            update_details(item_dict['details'], name_space, setup_space, parent_id=name)
        if 'visible_requirements' in item_dict:
            item.visible_requirements = requirements_from_dict(name, item_dict['visible_requirements'], name_space, setup_space)
        if 'target_responses' in item_dict:
            item.target_responses = action_responses_from_dict(name, item_dict['target_responses'], name_space)
        if 'tool_responses' in item_dict:
            item.tool_responses   = action_responses_from_dict(name, item_dict['tool_responses'],   name_space)
        if 'state_responses' in item_dict:
            item.state_responses  = state_responses_from_dict(name,  item_dict['state_responses'],  name_space)
    except ValueError as e:
        print(f"Error in item update {name}: {e}")
    
def update_items(item_dicts:list[dict[str,Any]], name_space:NameFinder, setup_space:NameFinder) -> None:
    [update_item(item_dict, name_space, setup_space) for item_dict in item_dicts]

# SKILL SET

def one_from_dict_skill_set(skill_dict:dict[str,Any|dict], name_space:NameFinder) -> dict[str,Any]:
    inputs = one_from_dict_named(skill_dict)
    skills = dict[Skill,int]()
    try:
        if 'skills' in skill_dict:
            for skill_id, skill_level in skill_dict['skills'].items():
                skill = name_space.get_from_id(skill_id, 'skill')
                skills[skill] = skill_level
        inputs['skills'] = skills
        inputs['default_proficiency'] = skill_dict.get('default_proficiency', None)
    except ValueError as e:
        print(f"Error in skill set {inputs['name']}: {e}")
    return inputs

def many_from_dict_skill_set(skill_dicts:dict[str,Any], name_space:NameFinder) -> list[dict[str,Any]]:
    return [one_from_dict_skill_set(skill_dict, name_space) for skill_dict in skill_dicts]

# CHARACTER

def one_from_dict_character(character_dict:dict[str,Any], name_space:NameFinder, setup_space:NameFinder) -> dict[str,Any]:
    inputs = one_from_dict_item(character_dict, name_space, setup_space)
    try:
        inputs['skills'] = name_space.get_from_id(character_dict['skills'], 'skillset') if 'skills' in character_dict else None
        inputs['achievements'] = input_list(character_dict['achievements'], name_space, 'achievement') if 'achievements' in character_dict else None
        inputs['type'] = character_dict.get('type', 'standard')
    except ValueError as e:
        print(f"Error in character {inputs['name']}: {e}")
    return inputs

def many_from_dict_character(character_dicts:list[dict[str,Any]], name_space:NameFinder, setup_space:NameFinder) -> list[dict[str,Any]]:
    return [one_from_dict_character(character_dict, name_space, setup_space) for character_dict in character_dicts]

def update_character(character_dict:dict[str,Any], name_space:NameFinder, setup_space:NameFinder) -> None:
    update_item(character_dict, name_space, setup_space)
    name = character_dict['name']
    id   = character_dict['id'] if 'id' in character_dict else name
    id   = id.lower()
    character = name_space.get_from_id(id)
    assert isinstance(character, Actor)
    try:
        if 'actor_responses' in character_dict:
            character.actor_responses = action_responses_from_dict(name, character_dict['actor_responses'], name_space)
        if 'inventory' in character_dict:
            inventory_inputs = one_from_dict_inventory(name, character_dict['inventory'], name_space)
            inventory = LocationDetail(**inventory_inputs)
            inventories = character.children.get_from_name('inventory')
            for inv in inventories:
                assert character.children.remove(inv)
            inventory.parent = character
            assert character.children.add(inventory)
            assert character.get_inventory() is not None
    except ValueError as e:
        print(f"Error in character update {name}: {e}")

def update_characters(character_dicts:list[dict[str,Any]], name_space:NameFinder, setup_space:NameFinder) -> None:
    [update_character(character_dict, name_space, setup_space) for character_dict in character_dicts]

# LOCATION DETAIL

def detail_id(id:str|None, name:str, parent_id:str) -> str:
    if parent_id is not None and id is None:
        return f"{name} {parent_id}".lower()
    return id

def one_from_dict_detail(detail_dict:dict[str,Any], *, parent_id:str=None) -> dict[str,Any]:
    inputs = one_from_dict_named(detail_dict)
    inputs['id'] = detail_id(inputs['id'], inputs['name'], parent_id)
    try:
        inputs['item_limit'] = item_limit_from_dict(detail_dict['item_limit']) if 'item_limit' in detail_dict else None
        inputs['hidden'] = detail_dict.get('hidden', None)
    except ValueError as e:
        print(f"Error in detail {inputs['name']}: {e}")
    return inputs

def many_from_dict_detail(detail_dicts:dict[str,Any], *, parent_id:str=None) -> list[dict[str,Any]]:
    return [one_from_dict_detail(detail_dict, parent_id=parent_id) for detail_dict in detail_dicts]

def update_detail(detail_dict:dict[str,Any], name_space:NameFinder, setup_space:NameFinder, *, parent_id:str=None) -> None:
    name = detail_dict['name']
    id   = detail_id(detail_dict.get('id', None), name, parent_id)
    if id is None:
        id = name
    detail = name_space.get_from_id(id)
    assert isinstance(detail, LocationDetail)
    try:
        if 'description' in detail_dict:
            detail.description = response_from_input(id, detail_dict['description'], name_space)
        if 'item_responses' in detail_dict:
            detail.item_responses = item_responses_from_dict(id, detail_dict['item_response'], name_space)
        if 'contents' in detail_dict:
            detail._set_children(children_from_dict(id, detail_dict['contents'], name_space))
        if 'visible_requirements' in detail_dict:
            detail.visible_requirements = requirements_from_dict(id, detail_dict['visible_requirements'], name_space, setup_space)
    except ValueError as e:
        print(f"Error in detail '{name}' ({id}) update: {e}")

def update_details(detail_dicts:list[dict[str,Any]], name_space:NameFinder, setup_space:NameFinder, *, parent_id:str=None) -> None:
    [update_detail(detail_dict, name_space, setup_space, parent_id=parent_id) for detail_dict in detail_dicts]

# PATHS

def path_id(id:str|None, name:str, direction_name:str, room_name:str) -> str:
    if id is None:
        return f"{name} going {direction_name} in {room_name}".lower()
    return id

def one_from_dict_path(path_dict:dict[str,Any|dict], name_space:NameFinder, room_name:str, direction_name:str) -> dict[str,Any]:
    inputs = one_from_dict_named(path_dict)
    try:
        inputs['id'] = path_id(inputs['id'], inputs['name'], direction_name, room_name)
        inputs['end'] = path_dict.get('end', None)
        path_type = 'single'
        if 'multi_end' in path_dict:
            path_type = 'multi'
            multi_end = dict[Target, str]()
            for item_id, room_name in path_dict['multi_end'].items():
                item = name_space.get_from_id(item_id)
                multi_end[item] = room_name
            inputs['multi_end'] = multi_end
        inputs['path_type'] = path_type
        inputs['hidden_when_locked'] = path_dict.get('hidden_when_locked', False)
        inputs['item_limit'] = item_limit_from_dict(path_dict['item_limit']) if 'item_limit' in path_dict else None
        inputs['description'] = None
    except ValueError as e:
        print(f"Error in path {inputs['name']}: {e}")
    return inputs
    
def update_path(path_dict:dict[str,Any], name_space:NameFinder, setup_space, room_name:str, direction_name:str) -> None:
    name = path_dict['name']
    id   = path_id(path_dict.get('id',None), name, direction_name, room_name)
    path = name_space.get_from_id(id)
    assert isinstance(path, Path)
    try:
        path._set_end(name_space)
        if 'exit_response' in path_dict:
            path.exit_response = response_from_input(name, path_dict['exit_response'], name_space)
        path.description = response_from_input(name, path_dict['description'], name_space)
        if 'visible_requirements' in path_dict:
            path.visible_requirements = requirements_from_dict(name, path_dict['visible_requirements'], name_space, setup_space)
        if 'passing_requirements' in path_dict:
            path.passing_requirements = requirements_from_dict(name, path_dict['passing_requirements'], name_space, setup_space)
        if 'path_items' in path_dict:
            path._set_children(children_from_dict(name, path_dict['path_items'], name_space))
        if 'item_responses' in path_dict:
            path.item_responses = item_responses_from_dict(name, path_dict['item_responses'], name_space)
    except ValueError as e:
        print(f"Error in path update {name}: {e}")

# LOCATION

def one_from_dict_location(location_dict:dict[str,Any|dict], name_space:NameFinder, setup_space:NameFinder) -> dict[str,Any]:
    inputs = one_from_dict_named(location_dict)
    name = inputs['name']
    paths = dict[Direction,Path]()
    try:
        if 'paths' in location_dict:
            for direction_id, path_dict in location_dict['paths'].items():
                direction = name_space.get_from_id(direction_id)
                path_inputs = one_from_dict_path(path_dict, name_space, name, direction.get_name())
                path_type = path_inputs['path_type']
                del path_inputs['path_type']
                if path_type == 'single':
                    path = SingleEndPath(**path_inputs)
                elif path_type == 'multi':
                    path = MultiEndPath(**path_inputs)
                else:
                    print(f"Error: unknown path type {path_type}")
                name_space.add(path)
                paths[direction] = path
        inputs['paths'] = paths
        detail_inputs = many_from_dict_detail(location_dict['details'], parent_id=name) if 'details' in location_dict else []
        details = [LocationDetail(**kwargs) for kwargs in detail_inputs]
        name_space.add_many(details)
        contents = details
        if 'contents' in location_dict:
            for child_id in location_dict['contents']:
                child = name_space.get_from_id(child_id, ['target', 'actor', 'locationdetail'])
                contents.append(child)
        inputs['children'] = contents
        inputs['start_location'] = location_dict.get('start', False)
        inputs['item_limit'] = item_limit_from_dict(location_dict['item_limit']) if 'item_limit' in location_dict else None
        inputs['description'] = None
    except ValueError as e:
        print(f"Error in location {inputs['name']}: {e}")
    return inputs

def many_from_dict_location(location_dicts:dict[str,Any], name_space:NameFinder, setup_space:NameFinder) -> list[dict[str,Any]]:
    return [one_from_dict_location(location_dict, name_space, setup_space) for location_dict in location_dicts]

def update_location(location_dict:dict[str,Any|dict], name_space:NameFinder, setup_space:NameFinder) -> None:
    name = location_dict['name']
    id   = location_dict['id'] if 'id' in location_dict else name
    id   = id.lower()
    location = name_space.get_from_id(id)
    assert isinstance(location, Location)
    try:
        if 'paths' in location_dict:
            for direction_id, path_dict in location_dict['paths'].items():
                direction = name_space.get_from_id(direction_id)
                update_path(path_dict, name_space, setup_space, name, direction.get_name())
        if 'details' in location_dict:
            update_details(location_dict['details'], name_space, setup_space, parent_id=name)
        if 'visible_requirements' in location_dict:
            location.visible_requirements = requirements_from_dict(name, location_dict['visible_requirements'], name_space, setup_space)
        if 'item_responses' in location_dict:
            location.item_responses = item_responses_from_dict(name, location_dict['item_responses'], name_space)
        if 'description' in location_dict:
            location.description = response_from_input(name, location_dict['description'], name_space)
        if 'direction_responses' in location_dict:
            location.direction_responses = direction_responses_from_dict(name, location_dict['direction_responses'], name_space)
    except ValueError as e:
        print(f"Error in location update {name}: {e}")

def update_locations(location_dicts:list[dict[str,Any|dict]], name_space:NameFinder, setup_space:NameFinder) -> None:
    [update_location(location_dict, name_space, setup_space) for location_dict in location_dicts]

# CHARACTER CONTROL

class CharacterControlFactory:

    def __init__(self):
        self.characters = dict[Actor,CharacterController]()

    def create_character(self, character:Actor, controller:CharacterController) -> None:
        self.characters[character] = controller
    
    def get_controller(self, character:Actor) -> Optional[CharacterController]:
        return self.characters.get(character, None)
    
    def many_from_dict(self, controller_dicts:list[dict[str,Any]], name_space:NameFinder) -> None:
        for controller_dict in controller_dicts:
            character = name_space.get_from_id(controller_dict['character'], 'actor')
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
