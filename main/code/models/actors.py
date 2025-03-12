from typing import Optional

from code.models.state  import State, Skill, FullState, SkillSet, LocationDetail
from code.models.action import Named, Action

# Should Items know which character has them?
# Should all Targets have weight? size? value?

class Target(Named):

    def __init__(self, name:str, description:str, states:FullState, target_responses:Optional[dict['Action',str]]=None, tool_responses:Optional[dict['Action',str]]=None, state_responses:Optional[dict[State,str]]=None, aliases:Optional[str]=None):
        super().__init__(name, aliases)
        self.description = description
        self.states = states
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

    def get_current_state(self) -> list[State]:
        return self.states.get_current_states()

    def get_actions_as_target(self) -> list['Action']:
        return self.states.get_available_actions_as_target()

    def perform_action_as_target(self, action:'Action') -> list[str]:
        response = list[str]()
        if action in self.target_responses:
            response.append(self.target_responses[action])
        new_states = self.states.perform_action_as_target(action)
        for new_state in new_states:
            if new_state in self.state_responses:
                response.append(self.state_responses[new_state])
        return response
    
    def perform_action_as_tool(self, action:'Action') -> list[str]:
        response = list[str]()
        if action in self.target_responses:
            response.append(self.tool_responses[action])
        new_states = self.states.perform_action_as_tool(action)
        for new_state in new_states:
            if new_state in self.state_responses:
                response.append(self.state_responses[new_state])
        return response
    
    def get_location(self) -> tuple['Location',LocationDetail]:
        return self.location, self.location_detail
    
    def _set_location(self, location:'Location', detail:LocationDetail, *, origin=False) -> None:
        self.location = location
        self.location_detail = detail
        if origin:
            self.origin = location

    def change_location(self, location:'Location', detail:Optional[LocationDetail]=None) -> None:
        detail = LocationDetail() if detail is None else detail
        self.location.remove_target(self)
        location.add_target(self, detail)

    def remove_location(self, location:'Location') -> bool:
        if self.location == location:
            self.location = None
            self.location_detail = None
            return True
        return False

class Actor(Target):

    def __init__(self, name:str, description:str, states:FullState, skills:SkillSet, actor_responses:Optional[dict['Action',str]]=None, target_responses:Optional[dict['Action',str]]=None, tool_responses:Optional[dict['Action',str]]=None, state_responses:Optional[dict[State,str]]=None, aliases:Optional[list[str]]=None):
        super().__init__(name, description, states, target_responses, tool_responses, state_responses, aliases)
        self.actor_responses = dict[Action,str]() if actor_responses is None else actor_responses
        self.skills = skills

    def __repr__(self):
        return f"[Actor {self.name}]\n\tOrigin: {self.origin.name}\n\tLoc: {self.location.name}\n\tDet: {self.location_detail}\n\tStates: {self.states}\n\tSkills: {self.skills}"

    def get_proficiency(self, skill:Skill) -> int:
        return self.skills.get_proficiency(skill)
    
    def practice_skill(self, skill:Skill, amount:int=1) -> int:
        return self.skills.practice_skill(skill, amount)
    
    def lose_proficiency(self, skill:Skill, amount:int=1) -> int:
        return self.skills.lose_proficiency(skill, amount)

    def get_actions_as_actor(self) -> list['Action']:
        return self.states.get_available_actions_as_actor()

    def perform_action_as_actor(self, action:'Action') -> list[str]:
        response = list[str]()
        if action in self.actor_responses:
            response.append(self.actor_responses[action])
        new_states = self.states.perform_action_as_actor(action)
        for new_state in new_states:
            if new_state in self.actor_responses:
                response.append(self.actor_responses[new_state])
        return response

class Direction(Named):
    """The Directions a Character can move to get from Room to Room.
    """
    def __init__(self, name:str, aliases:Optional[list[str]]=None):
        super().__init__(name, aliases)

    def __repr__(self):
        return f"[Direction {self.name}]"

class Path(Named):

    def __init__(self, name:str, description:str, end:'Location', hidden:bool=False, exit_response:Optional[str]=None, linked_targets:Optional[dict[Target,State]]=None, passing_requirements:Optional[dict[Actor,State]]=None, aliases:Optional[list[str]]=None):
        super().__init__(name, aliases)
        self.description = description
        self.end = end
        self.hidden = hidden
        self.linked_targets = dict[Target,State]() if linked_targets is None else linked_targets
        self.passing_requirements = dict[Actor,State]() if passing_requirements is None else passing_requirements
        self.exit_response = exit_response

    def __repr__(self):
        return f"[Path {self.name}]"

    def get_description(self) -> str:
        return self.description
    
    def set_end(self, end:'Location') -> None:
        self.end = end
    
    def get_end(self) -> 'Location':
        return self.end
    
    def is_hidden(self) -> bool:
        return self.hidden
    
    def can_pass(self, actor:Actor) -> tuple[bool,tuple[Target,State],str]:
        for state in self.passing_requirements:
            if state not in actor.get_current_state():
                return False, (actor, state), self.exit_response
        for item,state in self.linked_targets.items():
            if state not in item.get_current_state():
                return False, (item, state), self.exit_response
        return True, None, self.exit_response

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
    
    def contains(self, target:Target) -> tuple[bool,LocationDetail|None]:
        if target in self.contents:
            return True, self.contents[target]
        return False, None
    
    def get_contents(self) -> list[Target]:
        return self.contents.keys()
    
    def is_start_location(self) -> bool:
        return self.start_location
    
    def get_path(self, direction:Direction) -> tuple[Path,str]:
        path = None
        if direction in self.paths:
            path = self.paths[direction]
        response = None
        if direction in self.direction_responses:
            response = self.direction_responses[direction]
        if path is None or path.is_hidden():
            return None, response
        return path, response
