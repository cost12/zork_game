from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import NamedTuple

from frozendict import frozendict

from models.named import Action, Named

# Adding: effects, is this needed?
# To add update: class, factory, json, other classes

class Effect(Named):
    def __repr__(self):
        return f"[Effect {self.name}]"

class Achievement(Named):
    def __repr__(self):
        return f"[Achievement {self.name}]"

@dataclass(frozen=True)
class State(Named):
    actions_as_target:frozenset[Action]=field(default_factory=frozenset)
    actions_as_actor:frozenset[Action]=field(default_factory=frozenset)
    actions_as_tool:frozenset[Action]=field(default_factory=frozenset)

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.actions_as_target, frozenset):
            object.__setattr__(self, 'actions_as_target', frozenset(self.actions_as_target))
        if not isinstance(self.actions_as_actor, frozenset):
            object.__setattr__(self, 'actions_as_actor', frozenset(self.actions_as_actor))
        if not isinstance(self.actions_as_tool, frozenset):
            object.__setattr__(self, 'actions_as_tool', frozenset(self.actions_as_tool))

    @staticmethod
    def create_state(name:str, actions_as_target:list[Action], actions_as_actor:list[Action], actions_as_tool:list[Action], aliases:list[str]=None, name_id:str=None) -> 'State':
        if aliases is None:
            aliases = []
        aliases = [alias.lower() for alias in aliases]
        if name.lower() not in aliases:
            aliases.append(name.lower())
        if name_id is None:
            name_id = name.lower()
        name_id = name_id.lower()
        return State(name, frozenset(actions_as_target), frozenset(actions_as_actor), frozenset(actions_as_tool), tuple(aliases), name_id)

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.name_id

    def get_aliases(self) -> list[str]:
        return list(self.aliases)

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

@dataclass(frozen=True)
class StateGroup(Named):
    states : tuple[State,...] = field(kw_only=True)

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.states, tuple):
            object.__setattr__(self, 'states', tuple(self.states))

    def __repr__(self):
        return f"[StateGroup {self.name}]"

    def get_states(self) -> list[State]:
        return self.states

    def has_state(self, state:State) -> bool:
        return state in self.states

    def get_actions_as_actor(self) -> list[Action]:
        return [action for state in self.states for action in state.get_actions_as_actor()]

    def can_act_as_actor(self, action:Action) -> bool:
        return any(state.can_act_as_actor(action) for state in self.states)

    def get_actions_as_target(self) -> list[Action]:
        return [action for state in self.states for action in state.get_actions_as_target()]

    def can_act_as_target(self, action:Action) -> bool:
        return any(state.can_act_as_target(action) for state in self.states)

    def get_actions_as_tool(self) -> list[Action]:
        return [action for state in self.states for action in state.get_actions_as_tool()]

    def can_act_as_tool(self, action:Action) -> bool:
        return any(state.can_act_as_tool(action) for state in self.states)

@dataclass(frozen=True)
class StateGraph(Named):
    target_graph:frozendict[StateGroup,frozendict[Action,StateGroup]]=field(default_factory=frozendict)
    tool_graph:frozendict[StateGroup,frozendict[Action,StateGroup]]=field(default_factory=frozendict)
    actor_graph:frozendict[StateGroup,dict[Action,StateGroup]]=field(default_factory=frozendict)
    time_graph:frozendict[StateGroup,tuple[int,StateGroup]]=field(default_factory=frozendict)
    default_state:StateGroup=field(kw_only=True)

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.target_graph, frozendict):
            object.__setattr__(self, 'target_graph', frozendict({sg: frozendict(sub_dict) for sg, sub_dict in self.target_graph.items()}))
        if not isinstance(self.tool_graph, frozendict):
            object.__setattr__(self, 'tool_graph', frozendict({sg: frozendict(sub_dict) for sg, sub_dict in self.tool_graph.items()}))
        if not isinstance(self.actor_graph, frozendict):
            object.__setattr__(self, 'actor_graph', frozendict({sg: frozendict(sub_dict) for sg, sub_dict in self.actor_graph.items()}))
        if not isinstance(self.time_graph, frozendict):
            object.__setattr__(self, 'time_graph', frozendict({sg: tuple(others) for sg, others in self.time_graph.items()}))

    def get_default_state(self) -> StateGroup:
        return self.default_state

    def perform_action_as_actor(self, action:Action, current_state: StateGroup) -> tuple[bool,StateGroup]:
        if current_state in self.actor_graph:
            if action in self.actor_graph[current_state]:
                return True, self.actor_graph[current_state][action]
        return False, current_state

    def perform_action_as_target(self, action:Action, current_state: StateGroup) -> tuple[bool,StateGroup]:
        if current_state in self.target_graph:
            if action in self.target_graph[current_state]:
                return True, self.target_graph[current_state][action]
        return False, current_state

    def perform_action_as_tool(self, action:Action, current_state: StateGroup) -> tuple[bool,StateGroup]:
        if current_state in self.tool_graph:
            if action in self.tool_graph[current_state]:
                return True, self.tool_graph[current_state][action]
        return False, current_state

    def time_passes(self, current_state: StateGroup, time_in_state: int, time:int=1) -> tuple[bool,StateGroup]:
        time_in_state += time
        if current_state in self.time_graph:
            if time_in_state >= self.time_graph[current_state][0]:
                return True, self.time_graph[current_state][1]
        return False, current_state

class FullState(ABC, Named):

    @abstractmethod
    def time_passes(self, time:int) -> list[tuple[bool,State]]:
        pass

    @abstractmethod
    def get_current_states(self) -> list[State]:
        pass

    @abstractmethod
    def get_current_effects(self) -> list[Effect]:
        pass

    @abstractmethod
    def has_state(self, state:State) -> bool:
        pass

    @abstractmethod
    def has_effect(self, effect:Effect) -> bool:
        pass

    @abstractmethod
    def get_available_actions_as_target(self) -> list[Action]:
        pass

    @abstractmethod
    def get_available_actions_as_actor(self) -> list[Action]:
        pass

    @abstractmethod
    def get_available_actions_as_tool(self) -> list[Action]:
        pass

    @abstractmethod
    def can_act_as_target(self, action:Action) -> bool:
        pass

    @abstractmethod
    def can_act_as_actor(self, action:Action) -> bool:
        pass

    @abstractmethod
    def can_act_as_tool(self, action:Action) -> bool:
        pass

    @abstractmethod
    def perform_action_as_target(self, action:Action) -> list[tuple[bool,State]]:
        pass

    @abstractmethod
    def perform_action_as_actor(self, action:Action) -> list[tuple[bool,State]]:
        pass

    @abstractmethod
    def perform_action_as_tool(self, action:Action) -> list[tuple[bool,State]]:
        pass

class CurrentState(NamedTuple):
    state_graph: StateGraph
    current_state_group: StateGroup
    time_in_state: int

@dataclass(frozen=True)
class StateDisconnectedGraph(FullState):
    state_graphs:tuple[CurrentState,...] = field(kw_only=True)

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.state_graphs, tuple):
            object.__setattr__(self, 'state_graphs', tuple(self.state_graphs))

    def time_passes(self, time:int=1) -> list[StateGroup]:
        return [new_state_group for graph,state_group,current_time in self.state_graphs for new_state_group in graph.time_passes(state_group, current_time, time)]

    def get_current_states(self) -> list[State]:
        return [state for _,state_group,_ in self.state_graphs for state in state_group.get_states()]

    def get_current_effects(self) -> list[Effect]:
        raise RuntimeError("Unimplemented")

    def has_state(self, state:State) -> bool:
        return any(state_group.has_state(state) for _,state_group,_ in self.state_graphs)

    def has_effect(self, effect:Effect) -> bool:
        raise RuntimeError("Unimplemented")

    def get_available_actions_as_actor(self) -> list[Action]:
        return [action for _,state_group,_ in self.state_graphs for action in state_group.get_actions_as_actor()]

    def get_available_actions_as_target(self) -> list[Action]:
        return [action for _,state_group,_ in self.state_graphs for action in state_group.get_actions_as_target()]

    def get_available_actions_as_tool(self) -> list[Action]:
        return [action for _,state_group,_ in self.state_graphs for action in state_group.get_actions_as_tool()]

    def perform_action_as_actor(self, action:Action) -> list[State]:
        return [state for graph,state_group,_ in self.state_graphs for state in graph.perform_action_as_actor(action, state_group)]

    def perform_action_as_target(self, action:Action) -> list[tuple[bool,State]]:
        return [state for graph,state_group,_ in self.state_graphs for state in graph.perform_action_as_target(action, state_group)]

    def perform_action_as_tool(self, action:Action) -> list[tuple[bool,State]]:
        return [state for graph,state_group,_ in self.state_graphs for state in graph.perform_action_as_tool(action, state_group)]

    def can_act_as_target(self, action:Action) -> bool:
        raise RuntimeError("Unimplemented")

    def can_act_as_actor(self, action:Action) -> bool:
        raise RuntimeError("Unimplemented")

    def can_act_as_tool(self, action:Action) -> bool:
        raise RuntimeError("Unimplemented")

class Skill(Named):
    def __repr__(self):
        return f"[Skill {self.name}]"

@dataclass(frozen=True)
class SkillSet(Named):
    skills:frozendict[Skill,int]=field(default_factory=frozendict)
    default_proficiency:int=0

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.skills, frozendict):
            object.__setattr__(self, 'skills', frozendict(self.skills))

    def practice_skill(self, skill:Skill, amount:int=1) -> 'SkillSet':
        new_skills = self.skills
        if skill not in self.skills:
            new_skills = self.skills | {skill: self.default_proficiency}
        new_skills = new_skills | {skill: self.skills[skill] + amount}
        return SkillSet(new_skills, self.default_proficiency)

    def lose_proficiency(self, skill:Skill, amount:int=1) -> 'SkillSet':
        return self.practice_skill(skill, -amount)

    def get_proficiency(self, skill:Skill) -> int:
        if skill in self.skills:
            return self.skills[skill]
        return self.default_proficiency
