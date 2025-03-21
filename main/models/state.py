from typing import Optional
from dataclasses import dataclass

from models.action import Action, Named

# Adding: effects, is this needed?
# To add update: class, factory, json, other classes

class Effect(Named):
    
    def __init__(self, name:str, aliases:Optional[list[str]]=None):
        super().__init__(name, aliases)

    def __repr__(self):
        return f"[Effect {self.name}]"

@dataclass(frozen=True)
class State:
    name:str
    actions_as_target:frozenset[Action]
    actions_as_actor:frozenset[Action]
    actions_as_tool:frozenset[Action]

    def __repr__(self):
        return f"[State: {self.name}]\n\tTarget: {self.actions_as_target}\n\tActor: {self.actions_as_actor}"

    @staticmethod
    def create_state(name:str, actions_as_target:list[Action], actions_as_actor:list[Action], actions_as_tool:list[Action]) -> 'State':
        return State(name, frozenset(actions_as_target), frozenset(actions_as_actor), frozenset(actions_as_tool))

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
    
    def get_actions_as_tool(self) -> list[Action]:
        return list(self.actions_as_tool)
    
    def can_act_as_tool(self, action:Action) -> bool:
        return action in self.actions_as_tool

class StateGroup(Named):

    def __init__(self, name:str, states:list[State], aliases:Optional[list[str]]=None):
        super().__init__(name, aliases)
        self.states = states

    def __repr__(self):
        return f"[StateGroup {self.name}]\n\t{self.states}"
    
    def get_states(self) -> list[State]:
        return self.states
    
    def has_state(self, state:State) -> bool:
        return state in self.states

    def get_actions_as_actor(self) -> list[Action]:
        return [action for state in self.states for action in state.get_actions_as_actor()]
    
    def can_act_as_actor(self, action:Action) -> bool:
        return any([state.can_act_as_actor(action) for state in self.states])
    
    def get_actions_as_target(self) -> list[Action]:
        return [action for state in self.states for action in state.get_actions_as_target()]
    
    def can_act_as_target(self, action:Action) -> bool:
        return any([state.can_act_as_target(action) for state in self.states])
    
    def get_actions_as_tool(self) -> list[Action]:
        return [action for state in self.states for action in state.get_actions_as_tool()]
    
    def can_act_as_tool(self, action:Action) -> bool:
        return any([state.can_act_as_tool(action) for state in self.states])

class StateGraph(Named):

    def __init__(self, name:str, current_state:StateGroup, target_graph:dict[StateGroup,dict[Action,StateGroup]], tool_graph:dict[StateGroup,dict[Action,StateGroup]], actor_graph:dict[StateGroup,dict[Action,StateGroup]], time_graph:dict[StateGroup,tuple[int,StateGroup]]):
        super().__init__(name)
        self.current_state = current_state
        self.time_in_state = 0
        self.target_graph = target_graph
        self.actor_graph = actor_graph
        self.tool_graph = tool_graph
        self.time_graph = time_graph

    def __repr__(self):
        return f"[StateGraph {self.name}]\n\tCurrent: {self.current_state}\n\tTG: {self.target_graph}\n\tAG: {self.actor_graph}\n\t2G: {self.tool_graph}"

    def has_state(self, state:State) -> bool:
        return self.current_state.has_state(state)
    
    def get_current_states(self) -> list[State]:
        return self.current_state.get_states()

    def get_available_actions_as_actor(self) -> list[Action]:
        return self.current_state.get_actions_as_actor()
    
    def get_available_actions_as_target(self) -> list[Action]:
        return self.current_state.get_actions_as_target()
    
    def get_available_actions_as_tool(self) -> list[Action]:
        return self.current_state.get_actions_as_tool()

    def perform_action_as_actor(self, action:Action) -> list[State]:
        if self.current_state in self.actor_graph:
            if action in self.actor_graph[self.current_state]:
                old_state = self.current_state
                self.current_state = self.actor_graph[self.current_state][action]
                self.time_in_state = 0
                return [state for state in self.current_state.get_states() if not old_state.has_state(state)]
        return []

    def perform_action_as_target(self, action:Action) -> list[State]:
        if self.current_state in self.target_graph:
            if action in self.target_graph[self.current_state]:
                old_state = self.current_state
                self.current_state = self.target_graph[self.current_state][action]
                self.time_in_state = 0
                return [state for state in self.current_state.get_states() if not old_state.has_state(state)]                    
        return []
    
    def perform_action_as_tool(self, action:Action) -> list[State]:
        if self.current_state in self.tool_graph:
            if action in self.tool_graph[self.current_state]:
                old_state = self.current_state
                self.current_state = self.tool_graph[self.current_state][action]
                self.time_in_state = 0
                return [state for state in self.current_state.get_states() if not old_state.has_state(state)]
        return []
    
    def time_passes(self, time:int=1) -> list[State]:
        self.time_in_state += time
        if self.current_state in self.time_graph:
            if self.time_in_state >= self.time_graph[self.current_state][0]:
                old_state = self.current_state
                self.current_state = self.time_graph[self.current_state][1]
                self.time_in_state = 0
                return [state for state in self.current_state.get_states() if not old_state.has_state(state)]
        return []

class FullState(Named):

    def time_passes(self, time:int) -> list[tuple[bool,State]]:
        pass

    def get_current_states(self) -> list[State]:
        pass

    def get_current_effects(self) -> list[Effect]:
        pass

    def has_state(self, state:State) -> bool:
        pass

    def has_effect(self, effect:Effect) -> bool:
        pass

    def get_available_actions_as_target(self) -> list[Action]:
        pass

    def get_available_actions_as_actor(self) -> list[Action]:
        pass

    def get_available_actions_as_tool(self) -> list[Action]:
        pass

    def can_act_as_target(self, action:Action) -> bool:
        pass
    
    def can_act_as_actor(self, action:Action) -> bool:
        pass

    def can_act_as_tool(self, action:Action) -> bool:
        pass

    def perform_action_as_target(self, action:Action) -> list[tuple[bool,State]]:
        pass

    def perform_action_as_actor(self, action:Action) -> list[tuple[bool,State]]:
        pass

    def perform_action_as_tool(self, action:Action) -> list[tuple[bool,State]]:
        pass

class StateDisconnectedGraph(FullState):

    def __init__(self, name:str, state_graphs:list[StateGraph]):
        super().__init__(name)
        self.state_graphs = state_graphs

    def __repr__(self):
        return f"[SDG {self.name}]\n\t{self.state_graphs}"

    def add_graph(self, graph:StateGraph) -> None:
        self.state_graphs.append(graph)

    def add_graphs(self, graphs:'StateDisconnectedGraph') -> None:
        self.state_graphs.extend(graphs.state_graphs)

    def time_passes(self, time:int=1) -> list[State]:
        return [state for graph in self.state_graphs for state in graph.time_passes(time)]

    def get_current_states(self) -> list[State]:
        return [state for graph in self.state_graphs for state in graph.get_current_states()]
    
    def get_current_effects(self) -> list[Effect]:
        pass

    def has_state(self, state:State) -> bool:
        return any([graph.has_state(state) for graph in self.state_graphs])

    def has_effect(self, effect:Effect) -> bool:
        pass
    
    def get_available_actions_as_actor(self) -> list[Action]:
        return [action for graph in self.state_graphs for action in graph.get_available_actions_as_actor()]
    
    def get_available_actions_as_target(self) -> list[Action]:
        return [action for graph in self.state_graphs for action in graph.get_available_actions_as_target()]
    
    def get_available_actions_as_tool(self) -> list[Action]:
        return [action for graph in self.state_graphs for action in graph.get_available_actions_as_tool()]

    def perform_action_as_actor(self, action:Action) -> list[State]:
        return [state for graph in self.state_graphs for state in graph.perform_action_as_actor(action)] 

    def perform_action_as_target(self, action:Action) -> list[tuple[bool,State]]:
        return [state for graph in self.state_graphs for state in graph.perform_action_as_target(action)]
    
    def perform_action_as_tool(self, action:Action) -> list[tuple[bool,State]]:
        return [state for graph in self.state_graphs for state in graph.perform_action_as_tool(action)]

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
