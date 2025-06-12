from typing import Optional, TYPE_CHECKING
import random

from models.state       import State, Skill, FullState, SkillSet, Achievement
from models.named       import Named, Action, Direction
from models.requirement import ActionRequirement, ItemPlacementRequirement
from models.response    import ResponseString, StaticResponse, CombinationResponse
from utils.constants    import *
from utils.relator      import NameFinder

# HELPERS

def get_total_value(items:list['HasLocation']) -> float:
    return sum([item.get_value() for item in items])

def get_total_weight(items:list['HasLocation']) -> float:
    return sum([item.get_weight() for item in items])

def get_total_size(items:list['HasLocation']) -> float:
    return sum([item.get_size() for item in items])

# LOCATION DETAILS

class ItemLimit:
    def __init__(self, size_limit:float=None, weight_limit:float=None, value_limit:float=None):
        self.size_limit   = size_limit
        self.weight_limit = weight_limit
        self.value_limit  = value_limit

    def __repr__(self):
        return f"[ItemLimit {self.size_limit} {self.weight_limit} {self.value_limit}]"

    def fits(self, items:list['HasLocation']) -> bool:
        return (self.size_limit   is None or self.size_limit   >= get_total_size(items))   and \
               (self.weight_limit is None or self.weight_limit >= get_total_weight(items)) and \
               (self.value_limit  is None or self.value_limit  >= get_total_value(items))

    def can_add(self, item:'HasLocation', items:list['HasLocation']):
        return (self.size_limit   is None or self.size_limit   >= get_total_size(items)   + item.get_size())   and \
               (self.weight_limit is None or self.weight_limit >= get_total_weight(items) + item.get_weight()) and \
               (self.value_limit  is None or self.value_limit  >= get_total_value(items)  + item.get_value())

class HasLocation(Named):

    def __init__(self, name:str, *, hidden=False, parent:'HasLocation'=None, children:'list[HasLocation]'=None, origin:bool=False, item_limit:ItemLimit=None, visible_requirements:list[ActionRequirement]=None, item_responses:dict['HasLocation',str]=None, aliases:list[str]=None, id:str=None):
        super().__init__(name, aliases, id)
        self.parent = parent
        self._set_children(children)
        self.origin_parent = parent if origin else None

        self.hidden = hidden
        self.item_limit = ItemLimit() if item_limit is None else item_limit
        self.visible_requirements = list[ActionRequirement]() if visible_requirements is None else visible_requirements
        self.item_responses = dict[HasLocation,ResponseString]() if item_responses is None else item_responses

    # GETTERS

    def get_description_to(self, character:'Actor') -> ResponseString:
        child_descriptions = [child.get_description_to(character) for child in self.children.get_from_name() if (child.is_visible_to(character))]
        return CombinationResponse(responses=child_descriptions)

    def get_parent(self) -> 'HasLocation':
        return self.parent
    
    def get_child(self, child_id:str) -> 'HasLocation':
        return self.children.get_from_id(child_id)
    
    def get_special_child(self, child_name:str) -> 'HasLocation':
        if child_name in ['on','inside','inventory','wearing']:
            try:
                found = self.children.get_from_name(child_name)
            except KeyError:
                found = []
            if len(found) == 1:
                return found[0]
        return None
    
    def get_top_parent(self) -> 'HasLocation':
        if self.parent is None:
            return self
        return self.parent.get_top_parent()
    
    def is_in(self, location:'HasLocation') -> bool:
        if self == location:
            return True
        if self.parent is None:
            return False
        return self.parent.is_in(location)
    
    def get_weight(self) -> float:
        return sum([child.get_weight() for child in self.children.get_from_name()])
    
    def get_value(self) -> float:
        return sum([child.get_value() for child in self.children.get_from_name()])
    
    def get_size(self) -> float:
        return sum([child.get_size() for child in self.children.get_from_name()])

    # SET LOCATION

    def _set_children(self, children:list['HasLocation']=None) -> None:
        self.children = NameFinder['HasLocation']()
        if children is not None:
            self.children.add_many(children)
        for child in self.children.get_from_name():
            child.parent = self

    def set_location(self, parent:'HasLocation', *, origin=False) -> None:
        if self.parent is not None:
            self.parent.remove_child(self)
        self.parent = parent
        self.parent.children.add(self)
        if origin:
            self.origin_parent = parent

    def add_child(self, child:'HasLocation') -> tuple[bool,ResponseString]:
        if self.item_limit.can_add(child, list(self.children.get_from_name())):
            response=[]
            if not child.parent == self:
                success=True
                if child.parent is not None:
                    success,r = child.parent.remove_child(child)
                    if r is not None:
                        response.append(r)
                if success:
                    self.children.add(child)
                    child.parent = self
                    r2 = self.item_responses.get(child, None)
                    if r2 is not None:
                        response.append(r2)
                    return True, CombinationResponse(response)
            response.append(StaticResponse(f"You already have {child.get_id()}"))
            return False, CombinationResponse(response)
        return False, StaticResponse(f"The {child.get_name()} doesn't fit.")

    def remove_child(self, child:'HasLocation') -> tuple[bool,ResponseString]:
        return self.children.remove(child), None
    
    # VISIBILITY
    
    def is_visible_to(self, character:'Actor') -> bool:
        if self.hidden:
            return False
        if len(self.visible_requirements) == 0:
            return True
        return all([requirement.meets_requirement(character)[0] for requirement in self.visible_requirements])
    
    # CHECK CONTENTS

    def contains_item(self, item:'HasLocation') -> bool:
        if self.children.contains(item):
            return True
        for child in self.children.get_from_name():
            if child.contains_item(item):
                return True
        return False
    
    def contains_item_visible_to(self, item:'HasLocation', character:'Actor') -> bool:
        if self.is_visible_to(character):
            if item == self:
                return True
            for child in self.children.get_from_name():
                if child.contains_item_visible_to(item, character):
                    return True
        return False
    
    def list_contents_visible_to(self, character:'Actor') -> list['HasLocation']:
        if self.is_visible_to(character):
            try:
                inside = self.children.get_from_name('inside')
            except KeyError:
                inside = []
            if len(inside) == 1:
                inside = inside[0]
                if inside.is_visible_to(character):
                    return [grandchild for grandchild in inside.children.get_from_name() if grandchild.is_visible_to(character)]
            else:
                return [child for child in self.children.get_from_name() if child.is_visible_to(character)]
        return list[HasLocation]()

class LocationDetail(HasLocation):

    def __init__(self, name:str="default", description:ResponseString=None, *, hidden:bool=False, parent:'HasLocation'=None, children:list[HasLocation]=None, origin:bool=False, item_limit:ItemLimit=None, visible_requirements:list[ActionRequirement]=None, item_responses:dict['HasLocation',ResponseString]=None, aliases:list[str]=None, id:str=None):
        super().__init__(name, hidden=hidden, parent=parent, children=children, origin=origin, item_limit=item_limit, visible_requirements=visible_requirements, item_responses=item_responses, aliases=aliases, id=id)
        self.description = StaticResponse("") if description is None else description

    def __repr__(self):
        return f"[LocationDetail {self.name}]"

    def get_description_to(self, character:'Actor') -> ResponseString:
        if self.is_visible_to(character):
            return self.description
        return None
             
    def is_noteworthy(self) -> bool:
        return self.description is None or isinstance(self.description, StaticResponse) and len(self.description.response) == 0

# PATHS/LOCATION DETAILS

class Path(HasLocation):
    def __init__(self, name:str, description:ResponseString, *, parent:'HasLocation'=None, children:list[HasLocation]=None, origin:bool=False, item_limit:ItemLimit=None, visible_requirements:list[ActionRequirement]=None, item_responses:dict['HasLocation',str]=None, passing_requirements:list[ActionRequirement]=None, hidden_when_locked:bool=False, exit_response:ResponseString=None, aliases:Optional[list[str]]=None, id:str=None):
        super().__init__(name, parent=parent, children=children, origin=origin, item_limit=item_limit, visible_requirements=visible_requirements, item_responses=item_responses, aliases=aliases, id=id)
        self.description = description
        self.exit_response = exit_response
        self.passing_requirements = list[ActionRequirement]() if passing_requirements is None else passing_requirements
        self.hidden_when_locked = hidden_when_locked

    def __repr__(self):
        return f"[Path {self.name}]"
    
    def get_description_to(self, character:'Actor') -> ResponseString:
        if self.is_visible_to(character):
            return self.description
        return None
        
    def _list_ends(self) -> list['Location']:
        pass

    def get_end(self, character:'Actor') -> 'Location':
        pass
    
    def is_visible_to(self, character) -> bool:
        if not super().is_visible_to(character):
            return False
        if self.hidden_when_locked and not self.can_pass(character):
            return False
        return True
    
    def _set_end(self, name_space:NameFinder) -> None:
        for requirement in self.passing_requirements:
            if isinstance(requirement, ItemPlacementRequirement):
                for item, location_info in requirement.item_placements.items():
                    location_name, detail_name, needed, response = location_info
                    location = name_space.get_from_id(location_name)
                    detail = None if detail_name is None else name_space.get_from_id(detail_name)
                    requirement.item_placements[item] = (location, detail, needed, response)
    
    def can_pass(self, character:'Actor') -> tuple[bool,ResponseString]:
        for requirement in self.passing_requirements:
            can_pass, response = requirement.meets_requirement(character)
            if not can_pass:
                return False, response
        return True, self.exit_response

class MultiEndPath(Path):
    def __init__(self, name:str, description:ResponseString, *, end:'Location', multi_end:dict['Target','Location'], parent:'HasLocation'=None, children:list[HasLocation]=None, origin:bool=False, item_limit:ItemLimit=None, visible_requirements:list[ActionRequirement]=None, item_responses:dict['HasLocation',ResponseString]=None, passing_requirements:list[ActionRequirement]=None, hidden_when_locked:bool=False, exit_response:ResponseString=None, aliases:Optional[list[str]]=None, id:str=None):
        super().__init__(name, description, parent=parent, children=children, origin=origin, item_limit=item_limit, passing_requirements=passing_requirements, visible_requirements=visible_requirements, item_responses=item_responses, hidden_when_locked=hidden_when_locked, exit_response=exit_response, aliases=aliases, id=id)
        self.multi_end = multi_end
        self.default_end = end

    def _list_ends(self) -> list['Location']:
        ends = list(self.multi_end.values())
        if self.default_end is not None:
            ends.append(self.default_end)
        return ends

    def _set_end(self, name_space:NameFinder):
        super()._set_end(name_space)
        if self.default_end is not None:
            self.default_end = name_space.get_from_id(self.default_end)
        for target in self.multi_end.keys():
            self.multi_end[target] = name_space.get_from_id(self.multi_end[target])

    def can_pass(self, character:'Actor') -> tuple[bool,ResponseString]:
        can_pass, response = super().can_pass(character)
        if not can_pass:
            return False, response
        items_holding = len([1 for item in self.multi_end.keys() if character.contains_item(item)])
        return items_holding == 1 or items_holding == 0 and self.default_end is not None, self.exit_response

    def get_end(self, character:'Actor'):
        if self.can_pass(character):
            for item, location in self.multi_end.items():
                if character.contains_item(item):
                    return location
            return self.default_end
        return None

class SingleEndPath(Path):

    def __init__(self, name:str, description:ResponseString, *, end:'Location', parent:'HasLocation'=None, children:list[HasLocation]=None, origin:bool=False, item_limit:ItemLimit=None, visible_requirements:list[ActionRequirement]=None, item_responses:dict['HasLocation',ResponseString]=None, passing_requirements:list[ActionRequirement]=None, hidden_when_locked:bool=False, exit_response:ResponseString=None, aliases:Optional[list[str]]=None, id:str=None):
        super().__init__(name, description, parent=parent, children=children, origin=origin, item_limit=item_limit, passing_requirements=passing_requirements, visible_requirements=visible_requirements, item_responses=item_responses, hidden_when_locked=hidden_when_locked, exit_response=exit_response, aliases=aliases, id=id)
        self.end = end

    def _list_ends(self) -> list['Location']:
        return [self.end]
    
    def get_end(self, character:'Actor') -> 'Location':
        return self.end
    
    def _set_end(self, name_space:NameFinder) -> None:
        super()._set_end(name_space)
        end = self.end
        self.end = name_space.get_from_id(self.end)
        if self.end is None:
            print(f"{end} room not found")
            return False

# TARGETS

class Target(HasLocation):

    def __init__(self, name:str, description:ResponseString, states:FullState, *, weight:float=None, size:float=None, value:float=None, target_responses:Optional[dict[Action,ResponseString]]=None, tool_responses:Optional[dict['Action',ResponseString]]=None, state_responses:Optional[dict[State,ResponseString]]=None, parent:'HasLocation'=None, children:list[HasLocation]=None, origin:bool=False, visible_requirements:list[ActionRequirement]=None, item_responses:dict['HasLocation',ResponseString]=None, aliases:Optional[str]=None, id:str=None):
        super().__init__(name, parent=parent, children=children, origin=origin, visible_requirements=visible_requirements, item_responses=item_responses, aliases=aliases, id=id)
        self.description = description
        self.states = states
        self.weight = 1.0 if weight is None else weight
        self.size =   1.0 if size   is None else size
        self.value =  0.0 if value  is None else value
        self.target_responses = dict[Action,ResponseString]() if target_responses is None else target_responses
        self.tool_responses   = dict[Action,ResponseString]() if tool_responses   is None else tool_responses
        self.state_responses  = dict[State, ResponseString]() if state_responses  is None else state_responses

    def __repr__(self):
        return f"[Target {self.name}]"

    # HasLocation overrides

    def get_description_to(self, character:'Actor') -> ResponseString:
        if self.is_visible_to(character):
            return self.description
        return None

    def add_child(self, child:HasLocation) -> tuple[bool,ResponseString]:
        return False, None
    
    def remove_child(self, child:HasLocation) -> tuple[bool,ResponseString]:
        return False, None

    def get_weight(self):
        return super().get_weight() + self.weight

    def get_value(self) -> float:
        return super().get_value() + self.value

    def get_size(self) -> float:
        return self.size
    
    # ACCESS LOCATIONS

    def add_item(self, item:HasLocation, child:HasLocation) -> tuple[bool,ResponseString]:
        if self.children.contains(child):
            return child.add_child(item)
        return False, StaticResponse(f"{child.get_id()} does not exist")
    
    def remove_item(self, item:HasLocation, child:HasLocation) -> tuple[bool,ResponseString]:
        if self.children.contains(child):
            return child.remove_child(item)
        return False, None
    
    # OTHER

    def get_current_state(self) -> list[State]:
        return self.states.get_current_states()

    def get_actions_as_target(self) -> list[Action]:
        return self.states.get_available_actions_as_target()
    
    def get_actions_as_tool(self) -> list[Action]:
        return self.states.get_available_actions_as_tool()
    
    def get_target_response(self, action:Action) -> ResponseString:
        if action in self.target_responses:
            return self.target_responses[action]
        return None
    
    def get_tool_response(self, action:Action) -> ResponseString:
        if action in self.tool_responses:
            return self.tool_responses[action]
        return None

    def perform_action_as_target(self, action:Action) -> ResponseString:
        response = list[ResponseString]()
        new_states = self.states.perform_action_as_target(action)
        for new_state in new_states:
            if DEBUG_RESPONSE: print(f"Target: {self.name} {action} {new_state} {self.state_responses}")
            if new_state in self.state_responses:
                response.append(self.state_responses[new_state])
        return CombinationResponse(response, joiner="\n")
    
    def perform_action_as_tool(self, action:Action) -> list[ResponseString]:
        response = list[ResponseString]()
        new_states = self.states.perform_action_as_tool(action)
        for new_state in new_states:
            if new_state in self.state_responses:
                response.append(self.state_responses[new_state])
        return CombinationResponse(response, joiner="\n")

class Actor(Target):

    def __init__(self, name:str, description:ResponseString, type:str, states:FullState, skills:SkillSet, *, achievements:set[Achievement]=None, weight:float=None, size:float=None, value:float=None, actor_responses:Optional[dict['Action',ResponseString]]=None, target_responses:Optional[dict['Action',ResponseString]]=None, tool_responses:Optional[dict['Action',ResponseString]]=None, state_responses:Optional[dict[State,ResponseString]]=None, aliases:Optional[list[str]]=None, parent:'HasLocation'=None, children:list[HasLocation]=None, origin:bool=False, visible_requirements:list[ActionRequirement]=None, item_responses:dict['HasLocation',ResponseString]=None, id:str=None):
        super().__init__(name, description, states, weight=weight, size=size, value=value, target_responses=target_responses, tool_responses=tool_responses, state_responses=state_responses, parent=parent, children=children, origin=origin, visible_requirements=visible_requirements, item_responses=item_responses, aliases=aliases, id=id)
        self.actor_responses = dict[Action,ResponseString]() if actor_responses is None else actor_responses
        self.type = type
        self.skills = skills
        self.achievements = set[Achievement]() if achievements is None else achievements

        if self.get_inventory() is None:
            self.children.add(LocationDetail(name='inventory', description=StaticResponse(f"{name}'s inventory"), hidden=True))
        if self.get_inventory(inventory='wearing') is None:
            self.children.add(LocationDetail(name='wearing', description=StaticResponse(f"{name}'s wearing"), hidden=True))

    def __repr__(self):
        return f"[Actor {self.name}]"

    # GETTERS

    def get_type(self) -> str:
        return self.type

    # SKILL

    def get_proficiency(self, skill:Skill) -> int:
        return self.skills.get_proficiency(skill)
    
    def practice_skill(self, skill:Skill, amount:int=1) -> int:
        return self.skills.practice_skill(skill, amount)
    
    def lose_proficiency(self, skill:Skill, amount:int=1) -> int:
        return self.skills.lose_proficiency(skill, amount)

    # ACTIONS

    def get_actions_as_actor(self) -> list[Action]:
        return self.states.get_available_actions_as_actor()

    def get_actor_response(self, action:Action) -> ResponseString:
        if action in self.actor_responses:
            return self.actor_responses[action]
        return None

    def perform_action_as_actor(self, action:Action) -> ResponseString:
        response = list[ResponseString]()
        if action in self.actor_responses:
            response.append(self.actor_responses[action])
        new_states = self.states.perform_action_as_actor(action)
        for new_state in new_states:
            if new_state in self.actor_responses:
                response.append(self.actor_responses[new_state])
        return CombinationResponse(response, joiner="\n")

    # ACHIEVEMENTS

    def has_completed_achievement(self, achievement:Achievement) -> bool:
        return achievement in self.achievements
    
    def complete_achievement(self, achievement:Achievement) -> None:
        self.achievements.add(achievement)

    # INVENTORY

    def add_to_inventory(self, item:'Target', *, inventory='inventory') -> tuple[bool,ResponseString]:
        return self.get_inventory(inventory=inventory).add_child(item)
    
    def remove_from_inventory(self, item:'Target', placement:Optional[HasLocation]=None, *, inventory='inventory') -> tuple[bool,ResponseString]:
        if self.get_inventory(inventory=inventory).contains_item(item):
            if placement is None:
                item.set_location(self.get_top_parent())
                return True, None
            else:
                return placement.add_child(item)
        return False, StaticResponse(f"You don't have {item.get_name()}")
    
    def get_inventory_items(self, *, inventory='inventory') -> list[Target]:
        return list(self.get_inventory(inventory=inventory).children.get_from_name())
    
    def get_inventory(self, *, inventory='inventory') -> 'HasLocation':
        return self.get_special_child(inventory)
    
    def is_wearing(self, item:Target) -> bool:
        return self.get_inventory(inventory='wearing').contains_item(item)

# LOCATIONS

class Location(HasLocation):

    def __init__(self, name:str, description:ResponseString, paths:dict[Direction,Path], *, action_restrictions:dict[Action,list[ActionRequirement]]=None, direction_responses:dict[Direction,ResponseString]=None, start_location:bool=False, parent:'HasLocation'=None, children:list[HasLocation]=None, origin:bool=False, item_limit:ItemLimit=None, visible_requirements:list[ActionRequirement]=None, item_responses:dict['HasLocation',ResponseString]=None, aliases:Optional[str]=None, id:str=None):
        super().__init__(name, parent=parent, children=children, origin=origin, item_limit=item_limit, visible_requirements=visible_requirements, item_responses=item_responses, aliases=aliases, id=id)
        self.description = description
        self.paths = paths
        self.direction_responses = dict[Direction,ResponseString]() if direction_responses is None else direction_responses
        self.action_restrictions = dict[Action,list[ActionRequirement]]() if action_restrictions is None else action_restrictions
        self.start_location = start_location

    def __repr__(self):
        return f"[Location {self.name}]"

    def action_allowed(self, character:Actor, action:Action) -> tuple[bool,ResponseString]:
        if action in self.action_restrictions:
            for requirement in self.action_restrictions[action]:
                meets, response = requirement.meets_requirement(character)
                if not meets:
                    return False, response
        return True, None

    def get_description_to(self, actor:Actor) -> ResponseString:
        responses = [StaticResponse(f"[{self.name}]"), self.description]

        for direction,path in self.paths.items():
            if path.is_visible_to(actor):
                responses.append(path.get_description_to(actor))

        for child in self.children.get_from_name():
            if child.is_visible_to(actor) and not child == actor:
                if isinstance(child, Target):
                    responses.append(CombinationResponse([StaticResponse("There is "), child.get_description_to(actor)]))
                else:
                    responses.append(child.get_description_to(actor))
        return CombinationResponse(responses, joiner="\n")
    
    def can_interact_with(self, character:Actor, item:Target) -> bool:
        if character.contains_item(item):
            return True
        for child in self.children.get_from_name():
            if DEBUG_TAKE: print(f"{child} has {item}?")
            if child.contains_item_visible_to(item, character):
                if DEBUG_TAKE: print("yes")
                return True
            if DEBUG_TAKE: print("no")
        for path in self.paths.values():
            if path.contains_item_visible_to(item, character):
                return True
        return False
    
    def is_start_location(self) -> bool:
        return self.start_location

    def get_path(self, character:Actor, direction:Direction) -> tuple[Path,ResponseString]:
        path = None
        if direction in self.paths:
            path = self.paths[direction]
        if path is None:
            for direction2, path2 in self.paths.items():
                if direction2.get_name() == 'any':
                    path = path2
        if direction.get_name() == 'random':
            path = random.choice(list(self.paths.values()))
        response = self.direction_responses.get(direction, None)
        if path is None or not path.is_visible_to(character):
            return None, response
        return path, response

    def _get_path(self, direction:Direction) -> tuple[Path,ResponseString]:
        path = None
        if direction in self.paths:
            path = self.paths[direction]
        if path is None:
            for direction, path2 in self.paths.items():
                if direction.get_name() == 'any':
                    path = path2
        return path, self.direction_responses.get(direction, None)
