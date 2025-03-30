from typing import Optional

from models.state  import State, Skill, FullState, SkillSet, Feat
from models.action import Named, Action

# Should Items know which character has them?
# Should all Targets have weight? size? value?

class Target(Named):
    DEFAULT_WEIGHT = 1
    DEFAULT_SIZE   = 1
    DEFAULT_VALUE  = 0

    def __init__(self, name:str, description:str, states:FullState,*, weight:float=DEFAULT_WEIGHT, size:float=DEFAULT_SIZE, value:float=DEFAULT_VALUE, target_responses:Optional[dict['Action',str]]=None, tool_responses:Optional[dict['Action',str]]=None, state_responses:Optional[dict[State,str]]=None, aliases:Optional[str]=None):
        super().__init__(name, aliases)
        self.description = description
        self.states = states
        self.weight = weight
        self.size = size
        self.value = value
        self.target_responses = dict[Action,str]() if target_responses is None else target_responses
        self.tool_responses   = dict[Action,str]() if tool_responses   is None else tool_responses
        self.state_responses  = dict[State,str]()  if state_responses  is None else state_responses
        self.origin = None
        self.location = None
        self.location_detail = None

    def __repr__(self):
        return f"[Target {self.name}]\n\tOrig: {self.origin.name}\n\t{self.states}\n\tLoc: {self.location.name}\n\t{self.location_detail}"

    def get_description(self) -> str:
        return self.description
    
    def get_weight(self) -> float:
        return self.weight

    def get_value(self) -> float:
        return self.value

    def get_size(self) -> float:
        return self.size

    def get_current_state(self) -> list[State]:
        return self.states.get_current_states()

    def get_actions_as_target(self) -> list[Action]:
        return self.states.get_available_actions_as_target()
    
    def get_actions_as_tool(self) -> list[Action]:
        return self.states.get_available_actions_as_tool()
    
    def get_target_response(self, action:Action) -> Optional[str]:
        if action in self.target_responses:
            return self.target_responses[action]
        return None
    
    def get_tool_response(self, action:Action) -> Optional[str]:
        if action in self.tool_responses:
            return self.tool_responses[action]
        return None

    def perform_action_as_target(self, action:Action) -> list[str]:
        response = list[str]()
        new_states = self.states.perform_action_as_target(action)
        for new_state in new_states:
            if new_state in self.state_responses:
                response.append(self.state_responses[new_state])
        return response
    
    def perform_action_as_tool(self, action:Action) -> list[str]:
        response = list[str]()
        new_states = self.states.perform_action_as_tool(action)
        for new_state in new_states:
            if new_state in self.state_responses:
                response.append(self.state_responses[new_state])
        return response
    
    def get_location(self) -> tuple['Location','LocationDetail']:
        return self.location, self.location_detail
    
    def _set_location(self, location:'Location', detail:'LocationDetail', *, origin=False) -> None:
        self.location = location
        self.location_detail = detail
        if origin:
            self.origin = location

    def change_location(self, location:'Location', detail:Optional['LocationDetail']=None) -> None:
        detail = LocationDetail() if detail is None else detail
        self.location.remove_target(self)
        location.add_target(self, detail)

    def remove_location(self, location:'Location') -> bool:
        if self.location == location:
            self.location = None
            self.location_detail = None
            return True
        return False

class Inventory:
    """Stores a Character's Items
    """
    def __init__(self, size_limit:int, weight_limit:float, items:Optional[list[Target]]=None):
        self.size_limit = size_limit
        self.weight_limit = weight_limit
        assert items is None or (sum([item.get_size() for item in items]) <= self.size_limit and sum([item.get_weight() for item in items]) <= self.weight_limit)
        self.items = list[Target]() if items is None else items

    def get_items(self) -> list[Target]:
        return self.items
    
    def get_total_value(self) -> float:
        return sum([item.get_value() for item in self.items])
    
    def get_total_weight(self) -> float:
        return sum([item.get_weight() for item in self.items])
    
    def get_total_size(self) -> float:
        return sum([item.get_size() for item in self.items])
    
    def contains(self, item:Target) -> bool:
        return item in self.items
    
    def add_item(self, item:Target) -> bool:
        if item.get_size() + self.get_total_size() <= self.size_limit and item.get_weight() + self.get_total_weight():
            self.items.append(item)
            return True
        return False
    
    def drop_item(self, item:Target) -> bool:
        if item in self.items:
            self.items.remove(item)
            return True
        return False

class Actor(Target):
    DEFAULT_WEIGHT = 100
    DEFAULT_SIZE   = 100
    DEFAULT_VALUE  = 0

    def __init__(self, name:str, description:str, type:str, states:FullState, skills:SkillSet, inventory:Inventory, *, feats:set[Feat]=None, weight:float=DEFAULT_WEIGHT, size:float=DEFAULT_SIZE, value:float=DEFAULT_VALUE, actor_responses:Optional[dict['Action',str]]=None, target_responses:Optional[dict['Action',str]]=None, tool_responses:Optional[dict['Action',str]]=None, state_responses:Optional[dict[State,str]]=None, aliases:Optional[list[str]]=None):
        super().__init__(name, description, states, weight=weight, size=size, value=value, target_responses=target_responses, tool_responses=tool_responses, state_responses=state_responses, aliases=aliases)
        self.actor_responses = dict[Action,str]() if actor_responses is None else actor_responses
        self.inventory = inventory
        self.inventory_location = LocationDetail(f"{self.name}'s inventory", True, hidden=True)
        self.type = type
        self.skills = skills
        self.feats = set[Feat]() if feats is None else feats

    def __repr__(self):
        return f"[Actor {self.name}]\n\tOrigin: {self.origin.name}\n\tLoc: {self.location.name}\n\tDet: {self.location_detail}\n\tStates: {self.states}\n\tSkills: {self.skills}"

    def get_proficiency(self, skill:Skill) -> int:
        return self.skills.get_proficiency(skill)
    
    def practice_skill(self, skill:Skill, amount:int=1) -> int:
        return self.skills.practice_skill(skill, amount)
    
    def lose_proficiency(self, skill:Skill, amount:int=1) -> int:
        return self.skills.lose_proficiency(skill, amount)

    def get_actions_as_actor(self) -> list[Action]:
        return self.states.get_available_actions_as_actor()

    def get_actor_response(self, action:Action) -> Optional[str]:
        if action in self.actor_responses:
            return self.actor_responses[action]
        return None

    def perform_action_as_actor(self, action:Action) -> list[str]:
        response = list[str]()
        if action in self.actor_responses:
            response.append(self.actor_responses[action])
        new_states = self.states.perform_action_as_actor(action)
        for new_state in new_states:
            if new_state in self.actor_responses:
                response.append(self.actor_responses[new_state])
        return response
    
    def get_type(self) -> str:
        return self.type

    def _set_location(self, location, detail, *, origin=False):
        super()._set_location(location, detail, origin=origin)
        for item in self.inventory.get_items():
            item.change_location(location, self.inventory_location)

    def get_inventory_weight(self) -> float:
        return self.inventory.get_total_weight()
    
    def get_inventory_value(self) -> float:
        return self.inventory.get_total_value()
    
    def get_inventory_size(self) -> float:
        return self.inventory.get_total_size()
    
    def add_item_to_inventory(self, item:Target) -> bool:
        if self.inventory.add_item(item):
            item.change_location(self.location, self.inventory_location)
            return True
        return False
    
    def remove_item_from_inventory(self, item:Target, detail:Optional['LocationDetail']=None) -> tuple[bool,Optional[str]]:
        response = None
        if self.inventory.drop_item(item):
            item.change_location(self.location, detail)
            if detail is not None:
                response = detail.place_item(item)
            return True, response
        return False, response
    
    def get_inventory_items(self) -> list[Target]:
        return self.inventory.get_items()
    
    def is_holding(self, item:Target) -> bool:
        return self.inventory.contains(item)
    
    def has_completed_feat(self, feat:Feat) -> bool:
        return feat in self.feats
    
    def complete_feat(self, feat:Feat) -> None:
        self.feats.add(feat)

class Direction(Named):
    """The Directions a Character can move to get from Room to Room.
    """
    def __init__(self, name:str, aliases:Optional[list[str]]=None):
        super().__init__(name, aliases)

    def __repr__(self):
        return f"[Direction {self.name}]"

class PathRequirement():
    def can_pass(self, character:Actor) -> tuple[bool,str]:
        pass

class CharacterStateRequirement(PathRequirement):
    def __init__(self, states_needed:dict[State,tuple[bool,str]]):
        self.states_needed = states_needed

    def can_pass(self, character:Actor) -> tuple[bool,Optional[str]]:
        for state, tup in self.states_needed.items():
            needed, response = tup
            if not state in character.get_current_state() == needed:
                return False, response
        return True, None
    
class CharacterFeatRequirement(PathRequirement):
    def __init__(self, feats_needed:dict[Feat,tuple[bool,str]]):
        self.feats_needed = feats_needed

    def can_pass(self, character:Actor) -> tuple[bool,Optional[str]]:
        for feat, tup in self.feats_needed.items():
            needed, response = tup
            if not character.has_completed_feat(feat) == needed:
                return False, response
        return True, None
    
class ItemStateRequirement(PathRequirement):
    def __init__(self, item_states:dict[Target,dict[State,tuple[bool,str]]]):
        self.item_states_needed = item_states

    def can_pass(self, character:Actor) -> tuple[bool,Optional[str]]:
        for item, states_needed in self.item_states_needed.items():
            for state, tup in states_needed.items():
                needed, response = tup
                if not state in item.get_current_state() == needed:
                    return False, response
        return True, None
    
class ItemsHeldRequirement(PathRequirement):
    def __init__(self, items_needed:dict[Target,tuple[bool,str]]):
        self.items_needed = items_needed

    def can_pass(self, character:Actor) -> tuple[bool,Optional[str]]:
        for item, tup in self.items_needed.items():
            needed, response = tup
            if not character.is_holding(item) == needed:
                return False, response
        return True, None
    
class ItemPlacementRequirement(PathRequirement):
    def __init__(self, item_placements:dict[Target,tuple['Location',Optional['LocationDetail'],bool,str]]):
        self.item_placements = item_placements

    def can_pass(self, character:Actor):
        for item, placement_info in self.item_placements.items():
            location, detail, needed, response = placement_info
            matches = item.get_location() == (location, detail) or \
                      item.get_location()[0] == location and detail is None
            if not matches == needed:
                return False, response
        return True, None                

class Path(Named):
    def __init__(self, name:str, description:str, *, path_items:list[Target]=None, hidden:bool=False, exit_response:Optional[str]=None, passing_requirements:list[PathRequirement]=None, aliases:Optional[list[str]]=None):
        super().__init__(name, aliases)
        self.description = description
        self.hidden = hidden
        self.exit_response = exit_response
        self.passing_requirements = passing_requirements
        self.path_items = list[Target]() if path_items is None else path_items

    def __repr__(self):
        return f"[Path {self.name}]"
    
    def contains_item(self, item:Target) -> bool:
        return item in self.path_items

    def get_description(self) -> str:
        return self.description

    def get_end(self, character:Actor) -> 'Location':
        pass
    
    def is_hidden(self) -> bool:
        return self.hidden
    
    def _set_end(self, location_factory, location_detail_factory) -> None:
        for requirement in self.passing_requirements:
            if isinstance(requirement, ItemPlacementRequirement):
                for item, location_info in requirement.item_placements.items():
                    location_name, detail_name, needed, response = location_info
                    location = location_factory.get_location(location_name)
                    detail = None if detail_name is None else location_detail_factory.get_detail(detail_name)
                    requirement.item_placements[item] = (location, detail, needed, response)
    
    def can_pass(self, character:Actor) -> tuple[bool,Optional[str]]:
        # TODO: optional response strings based on the reason a character couldn't pass (instead of the tuple)
        if self.passing_requirements is not None:
            for requirement in self.passing_requirements:
                can_pass, response = requirement.can_pass(character)
                if not can_pass:
                    return False, response
        return True, self.exit_response

class MultiEndPath(Path):
    def __init__(self, name:str, description:str, end:'Location', multi_end:dict[Target,'Location'], hidden:bool=False, exit_response:Optional[str]=None, *, path_items:list[Target]=None, passing_requirements:list[PathRequirement]=None, aliases:Optional[list[str]]=None):
        super().__init__(name, description, hidden=hidden, exit_response=exit_response, path_items=path_items, passing_requirements=passing_requirements, aliases=aliases)
        self.multi_end = multi_end
        self.default_end = end

    def _set_end(self, location_factory, location_detail_factory):
        super()._set_end(location_factory, location_detail_factory)
        if self.default_end is not None:
            self.default_end = location_factory.get_location(self.default_end)
        for target in self.multi_end.keys():
            self.multi_end[target] = location_factory.get_location(self.multi_end[target])

    def can_pass(self, character:Actor) -> tuple[bool,Optional[str]]:
        can_pass, response = super().can_pass(character)
        if not can_pass:
            return False, response
        items_holding = len([1 for item in self.multi_end.keys() if character.is_holding(item)])
        return items_holding == 1 or items_holding == 0 and self.default_end is not None, self.exit_response

    def get_end(self, character:Actor):
        if self.can_pass(character):
            for item, location in self.multi_end.items():
                if character.is_holding(item):
                    return location
            return self.default_end
        return None

class SingleEndPath(Path):

    def __init__(self, name:str, description:str, end:'Location', hidden:bool=False, exit_response:Optional[str]=None, *, passing_requirements:list[PathRequirement]=None, path_items:list[Target]=None, aliases:Optional[list[str]]=None):
        super().__init__(name, description, hidden=hidden, exit_response=exit_response, path_items=path_items, passing_requirements=passing_requirements, aliases=aliases)
        self.end = end
    
    def get_end(self, character:Actor) -> 'Location':
        return self.end
    
    def _set_end(self, location_factory, location_detail_factory) -> None:
        super()._set_end(location_factory, location_detail_factory)
        self.end = location_factory.get_location(self.end)

class LocationDetail(Named):

    def __init__(self, name:str="default", description:str="", note_worthy:bool=False, hidden:bool=False, item_limit:int=None, responses:dict[Target,str]=None, hidden_when:tuple[Target,dict[State,bool]]=None, aliases:list[str]=None):
        super().__init__(name, aliases)
        self.description = description
        self.note_worthy = note_worthy
        self.item_limit = item_limit
        self.hidden = hidden
        self.responses = dict[Target, str]() if responses is None else responses
        self.hidden_when = hidden_when

    def __repr__(self):
        return f"[LocationDetail {self.name}]\n\t{self.description}\n\tN: {self.note_worthy} H: {self.hidden}"

    def is_note_worthy(self) -> bool:
        return self.note_worthy
    
    def get_description(self) -> str:
        return self.description
    
    def is_hidden(self) -> bool:
        if self.hidden_when is None:
            return self.hidden
        target, states = self.hidden_when
        for state, is_hidden in states.items():
            if state in target.get_current_state():
                return is_hidden
        return False
    
    def place_item(self, target:Target) -> Optional[str]:
        if target in self.responses:
            return self.responses[target]
        return None 

class Location(Named):

    def __init__(self, name:str, description:str, paths:dict[Direction,Path], direction_responses:dict[Direction,str], details:Optional[list[LocationDetail]]=None, contents:Optional[dict[Target,LocationDetail]]=None, start_location:bool=False):
        super().__init__(name)
        self.description = description
        self.paths = paths
        self.direction_responses = dict[Direction,str]() if direction_responses is not None else direction_responses
        self.details = list[LocationDetail]() if details is None else details
        self.contents = dict[Target,LocationDetail]() if contents is None else contents
        self.start_location = start_location

        for target,detail in self.contents.items():
            target._set_location(self,detail,origin=True)

    def __repr__(self):
        return f"[Location {self.name}]\n\tPaths: {self.paths}\n\tDetails: {self.details}\n\tContents: {self.contents}"

    def get_description(self, actor:Actor) -> str:
        full_description = self.description

        for direction,path in self.paths.items():
            if not path.is_hidden():
                full_description += f"\nTo the {direction.get_name()} {path.get_description()}."

        for target,detail in self.contents.items():
            if not target == actor and not detail.is_hidden():
                if detail.is_note_worthy():
                    full_description += f"\nThere is a {target.get_description()} {detail.get_description()}."
                else:
                    full_description += f"\nThere is a {target.get_description()}."
        return full_description

    def add_target(self, target:Target, detail:Optional[LocationDetail]=None) -> None:
        detail = LocationDetail() if detail is None else detail
        self.contents[target] = detail
        target._set_location(self, detail)

    def remove_target(self, target:Target) -> bool:
        if target in self.contents:
            del self.contents[target]
            target.remove_location(self)
            return True
        return False
    
    def contains(self, target:Target) -> tuple[bool,LocationDetail|Path|None]:
        if target in self.contents:
            return True, self.contents[target]
        for path in self.paths.values():
            if path.contains_item(target):
                return True, path
        return False, None
    
    def is_start_location(self) -> bool:
        return self.start_location

    def get_path(self, direction:Direction) -> tuple[Path,str]:
        path = None
        if direction in self.paths:
            path = self.paths[direction]
        if path is None:
            for direction, path2 in self.paths.items():
                if direction.get_name() == 'any':
                    path = path2
        response = None
        if direction in self.direction_responses:
            response = self.direction_responses[direction]
        if path is None or path.is_hidden():
            return None, response
        return path, response
