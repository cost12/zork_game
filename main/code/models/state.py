from typing import Optional
from dataclasses import dataclass

from code.models.action import Action, Named

# Actions as tool? Actions that can be performed with an item instead of to an item

@dataclass(frozen=True)
class State:
    name:str
    actions_as_target:frozenset[Action]
    actions_as_actor:frozenset[Action]

    def __repr__(self):
        return f"[State: {self.name}]\n\tTarget: {self.actions_as_target}\n\tActor: {self.actions_as_actor}"

    @staticmethod
    def create_state(name:str, actions_as_target:list[Action], actions_as_actor:list[Action]) -> 'State':
        return State(name, frozenset(actions_as_target), frozenset(actions_as_actor))

    def get_name(self) -> str:
        return self.name
    
    def get_actions_as_actor(self) -> list[Action]:
        return list(self.actions_as_actor)
    
    def can_act_as_actor(self, action:Action) -> bool:
        return action in self.actions_as_actor
    
    def get_actions_as_target(self) -> list[Action]:
        return list(self.actions_as_target)
    
    def can_act_as_target(self, action:Action) -> bool:
        return action in self.actions_as_target

class StateGraph(Named):

    def __init__(self, name:str, current_state:State, target_graph:dict[State,dict[Action,State]], actor_graph:dict[State,dict[Action,State]]):
        super().__init__(name)
        self.current_state = current_state
        self.target_graph = target_graph
        self.actor_graph = actor_graph

    def __repr__(self):
        return f"[StateGraph {self.name}]\n\tCurrent: {self.current_state}\n\tTG: {self.target_graph}\n\tAG: {self.actor_graph}"

    def get_current_state(self) -> State:
        return self.current_state

    def get_available_actions_as_actor(self) -> list[Action]:
        return self.current_state.get_actions_as_actor()
    
    def get_available_actions_as_target(self) -> list[Action]:
        return self.current_state.get_actions_as_target()

    def perform_action_as_actor(self, action:Action) -> tuple[bool,State]:
        if self.current_state.can_act_as_actor(action):
            if self.current_state in self.actor_graph:
                if action in self.actor_graph[self.current_state]:
                    self.current_state = self.actor_graph[self.current_state][action]
                return True, self.current_state
        return False, self.current_state

    def perform_action_as_target(self, action:Action) -> tuple[bool,State]:
        if self.current_state.can_act_as_target(action):
            if action in self.target_graph[self.current_state]:
                self.current_state = self.target_graph[self.current_state][action]
            return True, self.current_state
        return False, self.current_state

class StateDisconnectedGraph(Named):

    def __init__(self, name:str, state_graphs:list[StateGraph]):
        super().__init__(name)
        self.state_graphs = state_graphs

    def __repr__(self):
        return f"[SDG {self.name}]\n\t{self.state_graphs}"

    def add_graph(self, graph:StateGraph) -> None:
        self.state_graphs.append(graph)

    def add_graphs(self, graphs:'StateDisconnectedGraph') -> None:
        self.state_graphs.extend(graphs.state_graphs)

    def get_current_states(self) -> list[State]:
        return [graph.get_current_state() for graph in self.state_graphs]
    
    def get_available_actions_as_actor(self) -> list[Action]:
        return [action for graph in self.state_graphs for action in graph.get_available_actions_as_actor()]
    
    def get_available_actions_as_target(self) -> list[Action]:
        return [action for graph in self.state_graphs for action in graph.get_available_actions_as_target()]
    
    def perform_action_as_actor(self, action:Action) -> list[tuple[bool,State]]:
        return [graph.perform_action_as_actor(action) for graph in self.state_graphs] 

    def perform_action_as_target(self, action:Action) -> list[tuple[bool,State]]:
        return [graph.perform_action_as_target(action) for graph in self.state_graphs]

class Skill(Named):
    
    def __init__(self, name:str, aliases:Optional[list[str]]=None):
        super().__init__(name, aliases)

    def __repr__(self):
        return f"[Skill {self.name}]"

class SkillSet(Named):

    def __init__(self, name:str, skills:Optional[dict[Skill,int]]=None, default_proficiency:int=0):
        super().__init__(name)
        self.skills = dict[Skill,int]() if skills is None else skills
        self.default_proficiency = default_proficiency

    def __repr__(self):
        return f"[SkillSet {self.name}]\n\tSkills: {self.skills}\n\tDefault: {self.default_proficiency}"

    def practice_skill(self, skill:Skill, amount:int=1) -> int:
        if skill not in self.skills:
            self.skills[skill] = self.default_proficiency
        self.skills[skill] += amount

    def lose_proficiency(self, skill:Skill, amount:int=1) -> int:
        if skill not in self.skills:
            self.skills[skill] = self.default_proficiency
        self.skills[skill] -= amount

    def get_proficiency(self, skill:Skill) -> int:
        if skill in self.skills:
            return self.skills[skill]
        return self.default_proficiency

class LocationDetail(Named):

    def __init__(self, name:str="default", description:str="", note_worthy:bool=False, hidden:bool=False, item_limit:int=None, aliases:list[str]=None):
        super().__init__(name, aliases)
        self.description = description
        self.note_worthy = note_worthy
        self.item_limit = item_limit
        self.hidden = hidden

    def __repr__(self):
        return f"[LocationDetail {self.name}]\n\t{self.description}\n\tN: {self.note_worthy} H: {self.hidden}"

    def is_note_worthy(self) -> bool:
        return self.note_worthy
    
    def get_description(self) -> str:
        return self.description
    
    def is_hidden(self) -> bool:
        return self.hidden
