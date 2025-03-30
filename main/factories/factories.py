from typing import Optional, Any, Callable

from models.action    import Named, Action
from models.actors    import Location, Direction, Path, Target, Actor, Inventory, LocationDetail, SingleEndPath, MultiEndPath, Feat, PathRequirement, CharacterFeatRequirement, CharacterStateRequirement, ItemsHeldRequirement, ItemStateRequirement, ItemPlacementRequirement
from models.state     import State, StateGroup, StateGraph, StateDisconnectedGraph, Skill, SkillSet
from controls.character_control import CharacterController, CommandLineController, NPCController


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
                actions_as_target = [action_factory.get_named(action) for action in state['actions_as_target']]
            actions_as_tool = []
            if 'actions_as_tool' in state:
                actions_as_tool = [action_factory.get_named(action) for action in state['actions_as_tool']]
            actions_as_actor = []
            if 'actions_as_actor' in state:
                actions_as_actor  = [action_factory.get_named(action) for action in state['actions_as_actor']]
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
            states = [state_factory.get_state(state) for state in group_dict['states']]
            groups.append(self.create_state_group(name, states))
        return groups

class StateGraphFactory:

    def __init__(self):
        self.graphs  = dict[StateGraph,StateGraph]()
        self.aliases = dict[str,StateGraph]()

    def get_state_graphs(self) -> list[StateGraph]:
        return list(self.graphs.values())

    def create_state_graph(self, name:str, current_state:StateGroup, target_graph:dict[StateGroup,dict[Action,StateGroup]], tool_graph:dict[StateGroup,dict[Action,StateGroup]], actor_graph:dict[StateGroup,dict[Action,StateGroup]], time_graph:dict[StateGroup,tuple[int,StateGroup]]) -> StateGraph:
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
        return self.aliases.get(alias.lower(), None)
    
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
            target_graph = dict[StateGroup,dict[Action,StateGroup]]()
            if 'target_graph' in graph_dict:
                for state_group1_name in graph_dict['target_graph']:
                    state_group1 = state_group_factory.get_state_group(state_group1_name)
                    target_graph[state_group1] = dict[Action,StateGroup]()
                    for action_name in graph_dict['target_graph'][state_group1_name]:
                        action = action_factory.get_named(action_name)
                        state_group2 = state_group_factory.get_state_group(graph_dict['target_graph'][state_group1_name][action_name])
                        target_graph[state_group1][action] = state_group2
            tool_graph = dict[StateGroup,dict[Action,StateGroup]]()
            if 'tool_graph' in graph_dict:
                for state_group1_name in graph_dict['tool_graph']:
                    state_group1 = state_group_factory.get_state_group(state_group1_name)
                    tool_graph[state_group1] = dict[Action,StateGroup]()
                    for action_name in graph_dict['tool_graph'][state_group1_name]:
                        action = action_factory.get_named(action_name)
                        state_group2 = state_group_factory.get_state_group(graph_dict['tool_graph'][state_group1_name][action_name])
                        tool_graph[state_group1][action] = state_group2
            actor_graph = dict[StateGroup,dict[Action,StateGroup]]()
            if 'actor_graph' in graph_dict:
                for state_group1_name in graph_dict['actor_graph']:
                    state_group1 = state_group_factory.get_state_group(state_group1_name)
                    actor_graph[state_group1] = dict[Action,StateGroup]()
                    for action_name in graph_dict['actor_graph'][state_group1_name]:
                        action = action_factory.get_named(action_name)
                        state_group2 = state_group_factory.get_state_group(graph_dict['actor_graph'][state_group1_name][action_name])
                        actor_graph[state_group1][action] = state_group2
            time_graph = dict[StateGroup,tuple[int,StateGroup]]()
            if 'time_graph' in graph_dict:
                for state_group1_name in graph_dict['time_graph']:
                    state_group1 = state_group_factory.get_state_group(state_group1_name)
                    time,state_group2_name = graph_dict['time_graph'][state_group1_name]
                    state_group2 = state_group_factory.get_state_group(state_group2_name)
                    time_graph[state_group1] = (time, state_group2)
            graphs.append(self.create_state_graph(name, current_state, target_graph, tool_graph, actor_graph, time_graph))
        return graphs
    
class StateDisconnectedGraphFactory:

    def __init__(self):
        self.graphs  = dict[StateDisconnectedGraph,StateDisconnectedGraph]()
        self.aliases = dict[str,StateDisconnectedGraph]()

    def get_state_disconnected_graphs(self) -> list[StateDisconnectedGraph]:
        return list(self.graphs.values())

    def create_state_disconnected_graph(self, name:str, state_graphs:StateGraph) -> State:
        new_graph = StateDisconnectedGraph(name, state_graphs)
        if new_graph in self.graphs:
            return self.graphs[new_graph]
        for alias in new_graph.get_aliases():
            if alias in self.aliases:
                print(f"Error: two StateDisconnectedGraphs {self.aliases[alias]} and {new_graph} have the same name. Only one will be created.")
                return self.graphs[alias]
        self.graphs[new_graph] = new_graph
        for alias in new_graph.get_aliases():
            self.aliases[alias] = new_graph
        return new_graph
    
    def get_state_disconnected_graph(self, alias:str) -> Optional[StateGraph]:
        return self.aliases.get(alias.lower(), None)
    
    def many_from_dict(self, graph_dict:list[dict[str,Any]], state_graph_factory:StateGraphFactory) -> list[StateDisconnectedGraph]:
        graphs = list[StateDisconnectedGraph]()
        for graph in graph_dict:
            name = graph['name']
            state_graphs = [state_graph_factory.get_state_graph(graph) for graph in graph['state_graphs']]
            graphs.append(self.create_state_disconnected_graph(name, state_graphs))
        return graphs

class ItemFactory:

    def __init__(self):
        self.items = dict[Target,Target]()
        self.aliases = dict[str,Target]()

    def get_items(self) -> list[Target]:
        return list(self.items.values())

    def create_item(self, name:str, description:str, states:StateDisconnectedGraph, weight:float, value:float, size:float, target_responses:dict[Action,str], tool_responses:dict[Action,str], state_responses:dict[State,str]) -> Target:
        if size is None:
            size = Target.DEFAULT_SIZE
        if weight is None:
            weight = Target.DEFAULT_WEIGHT
        if value is None:
            value = Target.DEFAULT_VALUE
        new_item = Target(name, description, states, weight=weight, value=value, size=size, target_responses=target_responses, tool_responses=tool_responses, state_responses=state_responses)
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
    
    def many_from_dict(self, item_dicts:list[dict[str,Any]], state_graphs:StateDisconnectedGraphFactory, action_factory:NamedFactory[Action], state_factory:StateFactory) -> list[Target]:
        items = list[Target]()
        for item_dict in item_dicts:
            name = item_dict['name']
            description = item_dict['description']
            states = state_graphs.get_state_disconnected_graph(item_dict['states'])
            weight = None
            if 'weight' in item_dict:
                weight = item_dict['weight']
            value = None
            if 'value' in item_dict:
                value = item_dict['value']
            size = None
            if 'size' in item_dict:
                size = item_dict['size']
            target_responses = dict[Action,str]()
            if 'target_responses' in item_dict:
                for action_name in item_dict['target_responses']:
                    action = action_factory.get_named(action_name)
                    target_responses[action] = item_dict['target_responses'][action_name]
            tool_responses = dict[Action,str]()
            if 'tool_responses' in item_dict:
                for action_name in item_dict['tool_responses']:
                    action = action_factory.get_named(action_name)
                    tool_responses[action] = item_dict['tool_responses'][action_name]
            state_responses = dict[State,str]()
            if 'state_responses' in item_dict:
                for state_name in item_dict['state_responses']:
                    state = state_factory.get_state(state_name)
                    state_responses[state] = item_dict['state_responses'][state_name]
            items.append(self.create_item(name, description, states, weight, value, size, target_responses, tool_responses, state_responses))
        return items
    
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
                         description:str, 
                         type:str, 
                         states:StateDisconnectedGraph, 
                         skills:SkillSet,
                         inventory:Inventory,
                         weight:float,
                         size:float,
                         value:float,
                         actor_responses:dict[Action,str],
                         target_responses:dict[Action,str], 
                         tool_responses:dict[Action,str],
                         state_responses:dict[State,str],
                         feats:list[Feat],
                         aliases:list[str]) -> Actor:
        new_character = Actor(name, description, type, states, skills, inventory, weight=weight, size=size, value=value, actor_responses=actor_responses, target_responses=target_responses, tool_responses=tool_responses, state_responses=state_responses, feats=feats, aliases=aliases)
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
    
    def __inventory_from_dict(self, inventory_dict:dict[str,Any], item_factory:ItemFactory) -> Inventory:
        size_limit = inventory_dict['size_limit']
        weight_limit = inventory_dict['weight_limit']
        items = list[Target]()
        if 'items' in inventory_dict:
            for item_name in inventory_dict['items']:
                item = item_factory.get_item(item_name)
                items.append(item)
        return Inventory(size_limit, weight_limit, items)
    
    def many_from_dict(self, 
                       character_dicts:list[dict[str,Any]], 
                       state_graphs:StateDisconnectedGraphFactory,
                       skills_factory:SkillSetFactory,
                       item_factory:ItemFactory,
                       action_factory:NamedFactory[Action],
                       state_factory:StateFactory,
                       feat_factory:NamedFactory[Feat]) -> Actor:
        characters = list[Actor]()
        for character_dict in character_dicts:
            name = character_dict['name']
            description = character_dict['description']
            type = character_dict['type']
            states = state_graphs.get_state_disconnected_graph(character_dict['states'])
            skills = skills_factory.get_skill_set(character_dict['skills'])
            inventory = self.__inventory_from_dict(character_dict['inventory'], item_factory)
            weight = Actor.DEFAULT_WEIGHT
            if 'weight' in character_dict:
                weight = character_dict['weight']
            size = Actor.DEFAULT_SIZE
            if 'size' in character_dict:
                size = character_dict['size']
            value = Actor.DEFAULT_VALUE
            if 'value' in character_dict:
                value = character_dict['value']
            feats = list[Feat]()
            if 'feats' in character_dict:
                for feat_name in character_dict['feats']:
                    feats.append(feat_factory.get_named(feat_name))
            actor_responses = dict[Action,str]()
            if 'actor_responses' in character_dict:
                for action_name in character_dict['actor_responses']:
                    action = action_factory.get_named(action_name)
                    actor_responses[action] = character_dict['actor_responses'][action_name]
            target_responses = dict[Action,str]()
            if 'target_responses' in character_dict:
                for action_name in character_dict['target_responses']:
                    action = action_factory.get_named(action_name)
                    target_responses[action] = character_dict['target_responses'][action_name]
            tool_responses = dict[Action,str]()
            if 'tool_responses' in character_dict:
                for action_name in character_dict['tool_responses']:
                    action = action_factory.get_named(action_name)
                    tool_responses[action] = character_dict['tool_responses'][action_name]
            state_responses = dict[State,str]()
            if 'state_responses' in character_dict:
                for state_name in character_dict['state_responses']:
                    state = state_factory.get_state(state_name)
                    state_responses[state] = character_dict['state_responses'][state_name]
            aliases = None
            if 'aliases' in character_dict:
                aliases = character_dict['aliases']
            characters.append(self.create_character(name, description, type, states, skills, inventory, weight, size, value, actor_responses, target_responses, tool_responses, state_responses, feats, aliases))
        return characters

class LocationDetailFactory:

    def __init__(self):
        self.details = dict[LocationDetail,LocationDetail]()
        self.aliases = dict[str,LocationDetail]()

    def get_details(self) -> list[LocationDetail]:
        return list(self.details.values())

    def create_detail(self, name:str="default", description:str="", note_worthy:bool=False, hidden:bool=False, hidden_when:tuple[Target,dict[State,bool]]=None, responses:dict[Target,str]=None, aliases:list[str]=None) -> SkillSet:
        new_detail = LocationDetail(name=name, description=description, note_worthy=note_worthy, hidden=hidden, hidden_when=hidden_when, responses=responses, aliases=aliases)
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
    
    def one_from_dict(self, detail_dict:dict[str,Any], item_factory:ItemFactory, state_factory:StateFactory) -> LocationDetail:
        name = detail_dict['name']
        description = detail_dict['description']
        note_worthy = len(description) > 0
        hidden = False
        if 'hidden' in detail_dict:
            hidden = detail_dict['hidden']
        hidden_when = None
        if 'hidden_when' in detail_dict:
            target_name, states_dict = detail_dict['hidden_when']
            target = item_factory.get_item(target_name)
            states = dict[State,bool]()
            for state_name, is_hidden in states_dict.items():
                state = state_factory.get_state(state_name)
                states[state] = is_hidden
            hidden_when = (target, states)
        aliases = None
        responses = dict[Target,str]()
        if 'responses' in detail_dict:
            for item_name, response in detail_dict['responses'].items():
                item = item_factory.get_item(item_name)
                responses[item] = response
        if 'aliases' in detail_dict:
            aliases = detail_dict['aliases']
        return self.create_detail(name, description, note_worthy, hidden, hidden_when, responses, aliases=aliases)
    
    def many_from_dict(self, detail_dicts:list[dict[str,Any]], items:ItemFactory, states:StateFactory) -> list[LocationDetail]:
        details = list[LocationDetail]()
        for detail_dict in detail_dicts:
            details.append(self.one_from_dict(detail_dict, items, states))
        return details

class LocationFactory:

    def __init__(self):
        self.locations = dict[SkillSet,SkillSet]()
        self.aliases = dict[str,SkillSet]()

    def get_locations(self) -> list[Location]:
        return list(self.locations.values())

    def create_location(self,
                        name:str, 
                        description:str, 
                        paths:dict[Direction,Path], 
                        direction_responses:dict[Direction,str],
                        details:list[LocationDetail],
                        contents:dict[Target,Location],
                        start_location:bool) -> Location:
        new_location = Location(name, description, paths, direction_responses, details, contents, start_location)
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
    
    def __path_from_dict(self, path_dict:dict[str,Any], item_factory:ItemFactory, character_factory:CharacterFactory, state_factory:StateFactory, feat_factory:NamedFactory[Feat]) -> Path:
        name = path_dict['name']
        description = path_dict['description']
        path_type = None
        if 'end' in path_dict:
            path_type = 'restricted'
            end = path_dict['end']
        if 'multi_end' in path_dict:
            path_type = 'multi'
            multi_end = dict[Target, str]()
            for item_name, room_name in path_dict['multi_end']:
                item = item_factory.get_item(item_name)
                multi_end[item] = room_name
        if path_type is None:
            print(f"ERROR: path {name} has no type")
        hidden = False
        if 'hidden' in path_dict:
            hidden = path_dict['hidden']
        exit_response = None
        if 'exit_response' in path_dict:
            exit_response = path_dict['exit_response']
        
        passing_requirements = list[PathRequirement]()
        if 'character_state_requirements' in path_dict:
            states_needed = dict[State,tuple[bool,str]]()
            states_needed_raw = path_dict['character_state_requirements']
            for state_name, needed in states_needed_raw.items():
                state = state_factory.get_state(state_name)
                if isinstance(needed, bool):
                    states_needed[state] = (needed,None)
                else:
                    states_needed[state] = (needed[0], needed[1])
            passing_requirements.append(CharacterStateRequirement(states_needed))
        if 'character_feat_requirements' in path_dict:
            feats_needed = dict[Feat,tuple[bool,str]]()
            feats_needed_raw = path_dict['character_feat_requirements']
            for feat_name, needed in feats_needed_raw.items():
                feat = feat_factory.get_named(feat_name)
                if isinstance(needed, bool):
                    feats_needed[feat] = (needed,None)
                else:
                    feats_needed[feat] = (needed[0], needed[1])
            passing_requirements.append(CharacterFeatRequirement(feats_needed))
        if 'item_state_requirements' in path_dict:
            item_states = dict[Target,dict[State,tuple[bool,str]]]()
            item_states_raw = path_dict['item_state_requirements']
            for item_name, states_needed_raw in item_states_raw.items():
                item = item_factory.get_item(item_name)
                states_needed = dict[State,tuple[bool,str]]()
                for state_name, needed in states_needed_raw.items():
                    state = state_factory.get_state(state_name)
                    if isinstance(needed, bool):
                        states_needed[state] = (needed,None)
                    else:
                        states_needed[state] = (needed[0], needed[1])
                item_states[item] = states_needed
            passing_requirements.append(ItemStateRequirement(item_states))
        if 'items_held_requirements' in path_dict:
            items_needed = dict[Target,tuple[bool,str]]()
            items_needed_raw = path_dict['items_held_requirements']
            for item_name, needed in items_needed_raw.items():
                item = item_factory.get_item(item_name)
                if isinstance(needed, bool):
                    items_needed[item] = (needed,None)
                else:
                    items_needed[item] = (needed[0], needed[1])
            passing_requirements.append(ItemsHeldRequirement(items_needed))
        if 'item_placement_requirements' in path_dict:
            item_placements = dict[Target,tuple['Location',Optional['LocationDetail'],bool,str]]()
            item_placements_raw = path_dict['item_placement_requirements']
            for item_name, location_info in item_placements_raw.items():
                item = item_factory.get_item(item_name)
                location_name = location_info[0]
                detail_name = None
                needed = location_info[1]
                response = None
                if isinstance(location_info[1], str):
                    detail_name = location_info[1]
                    needed = location_info[2]
                if isinstance(location_info[-1], str):
                    response = location_info[-1]
                item_placements[item] = (location_name, detail_name, needed, response)
            passing_requirements.append(ItemPlacementRequirement(item_placements))
        
        aliases = None
        if 'aliases' in path_dict:
            aliases = path_dict['aliases']
        if path_type == 'restricted':
            return SingleEndPath(name, description, end, hidden, exit_response, passing_requirements=passing_requirements, aliases=aliases)
        elif path_type == 'multi':
            return MultiEndPath(name, description, end, multi_end, hidden, exit_response, passing_requirements=passing_requirements, aliases=aliases)

    def many_from_dict(self, location_dicts:list[dict[str,Any]], character_factory:CharacterFactory, item_factory:ItemFactory, direction_factory:NamedFactory[Direction], state_factory:StateFactory, feat_factory:NamedFactory[Feat]) -> list[Location]:
        locations = list[Location]()
        for location_dict in location_dicts:
            name = location_dict['name']
            description = location_dict['description']
            paths = dict[Direction,Path]()
            if 'paths' in location_dict:
                for direction_name, path_dict in location_dict['paths'].items():
                    direction = direction_factory.get_named(direction_name)
                    path = self.__path_from_dict(path_dict, item_factory, character_factory, state_factory, feat_factory)
                    paths[direction] = path
            direction_responses = dict[Direction,str]()
            if 'direction_responses' in location_dict:
                for direction_name,response in location_dict['direction_responses'].items():
                    direction = direction_factory.get_named(direction)
                    direction_responses[direction] = response
            detail_factory = LocationDetailFactory()
            if 'details' in location_dict:
                detail_factory.many_from_dict(location_dict['details'], item_factory, state_factory)
            contents = dict[Target,LocationDetail]()
            if 'contents' in location_dict:
                for target_name,detail_name in location_dict['contents'].items():
                    target = character_factory.get_character(target_name)
                    if target is None:
                        target = item_factory.get_item(target_name)
                    if detail_name == "default":
                        detail = detail_factory.create_detail()
                    else:
                        detail = detail_factory.get_detail(detail_name)
                    contents[target] = detail
            start_location = False
            if 'start' in location_dict:
                start_location = bool(location_dict['start'])
            locations.append(self.create_location(name, description, paths, direction_responses, detail_factory.get_details(), contents, start_location))
        
        # for each path set the end to the correct location
        # (this can't be done earlier because the end location might not exist yet)
        for location_dict in location_dicts:
            location = self.get_location(location_dict['name'])
            if 'paths' in location_dict:
                for direction_name,path_dict in location_dict['paths'].items():
                    direction = direction_factory.get_named(direction_name)
                    location.get_path(direction)[0]._set_end(self, detail_factory)
        return locations

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
