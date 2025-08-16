from typing      import TypeVar
from dataclasses import dataclass, field
import networkx  as nx

from models.state               import State, Skill, FullState, SkillSet, Achievement
from models.named               import Named, Action, Direction, NameInfo
from readin.restriction_helpers import Restriction, RestrictionContext
from readin.description_helpers import Description, DescriptionContext, CombinationDescription, CombinationContext, plain_text_description

T = TypeVar('T')

def can_fit(item:'HasLocation', container:'HasLocation', item_tree:'ItemTree') -> bool:
    limit = container.get_item_limit()
    if     (limit.weight_limit is None or item_tree.get_weight(item) + item_tree.get_weight_of_contents(container) <= limit.weight_limit) \
        or (limit.size_limit   is None or item_tree.get_size(item)   + item_tree.get_size_of_contents(container)   <= limit.size_limit) \
        or (limit.value_limit  is None or item_tree.get_value(item)  + item_tree.get_value_of_contents(container)  <= limit.value_limit):
        return all(can_fit(item, c, item_tree) for c in item_tree.get_parents(container))
    return False

@dataclass
class ItemLimit:
    size_limit   : float|None = None
    weight_limit : float|None = None
    value_limit  : float|None = None

@dataclass
class VisibleInfo:
    hidden               : bool              = False
    visible_restrictions : list[Restriction] = field(default_factory=list[Restriction])

@dataclass
class ContainerInfo:
    item_limit     : ItemLimit               = field(default_factory=ItemLimit)
    item_responses : dict['HasLocation',str] = field(default_factory=dict['HasLocation',str])
    weight         : float                   = 1.0
    size           : float                   = 1.0
    value          : float                   = 0.0

class HasLocation(Named):

    def __init__(self, name_info:NameInfo, *, visible_info:VisibleInfo, container_info:ContainerInfo):
        super().__init__(name_info)
        self.visible_info = visible_info
        self.container_info = container_info

    def is_visible(self, context:RestrictionContext) -> tuple[bool,Description]:
        for visible_restriction in self.visible_info.visible_restrictions:
            passes, response = visible_restriction.passes(context)
            if not passes:
                return passes, response
        return False, None

    def get_weight(self) -> float:
        return self.container_info.weight

    def get_value(self) -> float:
        return self.container_info.value

    def get_size(self) -> float:
        return self.container_info.size

    def get_item_limit(self) -> ItemLimit:
        return self.container_info.item_limit

class LocationDetail(HasLocation):

    def __repr__(self):
        return f"<LocationDetail {self.get_name()}>"

@dataclass
class PathInfo:
    start                : 'Location'
    end                  : 'Location'
    direction            : Direction
    passing_restrictions : list[Restriction] = field(default_factory=list[Restriction])
    exit_response        : Description       = None
    hidden_when_locked   : bool              = False

@dataclass
class PathEndContext:
    character : 'Actor'
    inventory : 'ItemTree'
    start     : 'Location'

class Path(HasLocation):
    def __init__(self, name_info:NameInfo, path_info:PathInfo, *, visible_info:VisibleInfo, container_info:ContainerInfo):
        super().__init__(name_info, visible_info=visible_info, container_info=container_info)
        self.path_info = path_info

    def __repr__(self):
        return f"<Path {self.get_name()}>"

    def get_direction(self) -> Direction:
        return self.path_info.direction

    def get_start(self) -> 'Location':
        return self.path_info.start

    def list_starts(self) -> list[tuple['Location',Direction]]:
        return [(self.path_info.start, self.path_info.direction)]

    def get_end(self, context:PathEndContext) -> 'Location'|None:
        return self.path_info.end

    def can_pass(self, context:RestrictionContext) -> tuple[bool,Description]:
        for restriction in self.path_info.passing_restrictions:
            passes, response = restriction.passes(context)
            if not passes:
                return passes, response
        return True, None

class TwoWayPath(Path):
    def __init__(self, name_info:NameInfo, path_info:PathInfo, reverse_direction:Direction, *, visible_info:VisibleInfo, container_info:ContainerInfo):
        super().__init__(name_info, path_info, visible_info=visible_info, container_info=container_info)
        self.reverse_direction = reverse_direction

    def list_starts(self) -> list[tuple['Location',Direction]]:
        return [(self.path_info.start,self.path_info.direction), (self.path_info.end,self.reverse_direction)]

    def get_end(self, context:PathEndContext) -> 'Location'|None:
        if context.start == self.path_info.start:
            return self.path_info.end
        return self.path_info.start

class MultiPath(Path):
    def __init__(self, name_info:NameInfo, path_info:PathInfo, multi_end:dict['Target','Location'], *, visible_info:VisibleInfo, container_info:ContainerInfo):
        super().__init__(name_info, visible_info=visible_info, container_info=container_info, path_info=path_info)
        self.multi_end = multi_end

    def can_pass(self, context:RestrictionContext) -> tuple[bool,Description]:
        can_pass, response = super().can_pass(context)
        if not can_pass:
            return can_pass, response
        inventory = context.inventory.get_inventory_contents(context.character)
        overlap   = [item for item in inventory if item in self.multi_end]
        if len(overlap) == 0:
            if self.path_info.end:
                return True, None
            return False, plain_text_description("As far as you can see, this path has no end.")
        if len(overlap) == 1:
            return True, None
        return False, plain_text_description("The path stretches ahead like a maze and you dare not step forward.")

    def get_end(self, context:PathEndContext) -> 'Location'|None:
        inventory = context.inventory.get_inventory_contents(context.character)
        overlap   = [item for item in inventory if item in self.multi_end]
        if len(overlap) == 0:
            return self.path_info.end
        if len(overlap) == 1:
            return overlap[0]
        return None

@dataclass
class TargetInfo:
    states           : FullState
    target_responses : dict[Action,Description] = field(default_factory=dict)
    tool_responses   : dict[Action,Description] = field(default_factory=dict)
    state_responses  : dict[State, Description] = field(default_factory=dict)
    inside           : LocationDetail|None      = None
    on               : LocationDetail|None      = None

class Target(HasLocation):

    def __init__(self, name_info:NameInfo, target_info:TargetInfo, *, container_info:ContainerInfo, visible_info:VisibleInfo):
        super().__init__(name_info, visible_info=visible_info, container_info=container_info)
        self.target_info = target_info

    def __repr__(self):
        return f"<Target {self.get_name()}>"

    def get_inside(self) -> LocationDetail|None:
        return self.target_info.inside

    def get_on(self) -> LocationDetail|None:
        return self.target_info.on

    def get_current_state(self) -> list[State]:
        return self.target_info.states.get_current_states()

    def get_actions_as_target(self) -> list[Action]:
        return self.target_info.states.get_available_actions_as_target()

    def get_actions_as_tool(self) -> list[Action]:
        return self.target_info.states.get_available_actions_as_tool()

    def get_target_response(self, action:Action) -> Description:
        if action in self.target_info.target_responses:
            return self.target_info.target_responses[action]
        return None

    def get_tool_response(self, action:Action) -> Description:
        if action in self.target_info.tool_responses:
            return self.target_info.tool_responses[action]
        return None

    def perform_action_as_target(self, action:Action) -> Description:
        response = list[Description]()
        new_states = self.target_info.states.perform_action_as_target(action)
        for new_state in new_states:
            if new_state in self.target_info.state_responses:
                response.append(self.target_info.state_responses[new_state])
        return Description[CombinationContext](CombinationContext(response), CombinationDescription())

    def perform_action_as_tool(self, action:Action) -> list[Description]:
        response = list[Description]()
        new_states = self.target_info.states.perform_action_as_tool(action)
        for new_state in new_states:
            if new_state in self.target_info.state_responses:
                response.append(self.target_info.state_responses[new_state])
        return CombinationDescription[CombinationContext](CombinationContext(response), CombinationContext)

@dataclass
class ActorInfo:
    skills          : SkillSet
    inventory       : LocationDetail
    wearing         : LocationDetail
    achievements    : set[Achievement]         = field(default_factory=list)
    actor_responses : dict[Action,Description] = field(default_factory=dict)
    actor_type      : str                      = 'Standard'

class Actor(Target):

    def __init__(self, name_info:NameInfo, target_info:TargetInfo, actor_info:ActorInfo, *, container_info:ContainerInfo, visible_info:VisibleInfo):
        super().__init__(name_info, target_info, container_info=container_info, visible_info=visible_info)
        self.actor_info = actor_info

    def __repr__(self):
        return f"<Actor {self.get_name()}>"

    # GETTERS

    def get_type(self) -> str:
        return self.actor_info.actor_type

    def get_inventory(self) -> LocationDetail:
        return self.actor_info.inventory

    def get_wearing(self) -> LocationDetail:
        return self.actor_info.wearing

    # SKILL

    def get_proficiency(self, skill:Skill) -> int:
        return self.actor_info.skills.get_proficiency(skill)

    def practice_skill(self, skill:Skill, amount:int=1) -> int:
        return self.actor_info.skills.practice_skill(skill, amount)

    def lose_proficiency(self, skill:Skill, amount:int=1) -> int:
        return self.actor_info.skills.lose_proficiency(skill, amount)

    # ACTIONS

    def get_actions_as_actor(self) -> list[Action]:
        return self.target_info.states.get_available_actions_as_actor()

    def get_actor_response(self, action:Action) -> Description:
        if action in self.actor_info.actor_responses:
            return self.actor_info.actor_responses[action]
        return None

    def perform_action_as_actor(self, action:Action) -> Description:
        response = list[Description]()
        if action in self.actor_info.actor_responses:
            response.append(self.actor_info.actor_responses[action])
        new_states = self.target_info.states.perform_action_as_actor(action)
        for new_state in new_states:
            if new_state in self.actor_info.actor_responses:
                response.append(self.actor_info.actor_responses[new_state])
        return Description[CombinationContext](CombinationContext(response), CombinationDescription())

    # ACHIEVEMENTS

    def has_completed_achievement(self, achievement:Achievement) -> bool:
        return achievement in self.actor_info.achievements

    def complete_achievement(self, achievement:Achievement) -> None:
        self.actor_info.achievements.add(achievement)

@dataclass
class LocationInfo:
    is_start_location   : bool                           = False
    action_restrictions : dict[Action,list[Restriction]] = field(default_factory=dict)
    direction_responses : dict[Direction,Description]    = field(default_factory=dict)

class Location(HasLocation):

    def __init__(self, name_info:NameInfo, location_info:LocationInfo, container_info:ContainerInfo, visible_info:VisibleInfo):
        super().__init__(name_info, visible_info=visible_info, container_info=container_info)
        self.location_info = location_info

    def __repr__(self):
        return f"<Location {self.get_name()}>"

    def action_allowed(self, context:RestrictionContext, action:Action) -> tuple[bool,Description]:
        if action in self.location_info.action_restrictions:
            for requirement in self.location_info.action_restrictions[action]:
                meets, response = requirement.passes(context)
                if not meets:
                    return False, response
        return True, None

    def is_start_location(self) -> bool:
        return self.location_info.is_start_location

class ItemTree:
    def __init__(self):
        self.graph = nx.DiGraph()

    # initialization

    def add_room(self, room:Location):
        self.graph.add_node(room.get_id(), obj=room, type="room")

    def __add_edge(self, child:HasLocation, parent:HasLocation):
        self.graph.add_edge(parent.get_id(), child.get_id(), relationship="child")

    def add_location_detail(self, location_detail:LocationDetail, location:HasLocation):
        self.graph.add_node(location_detail.get_id(), obj=location_detail, type='location_detail')
        self.__add_edge(location_detail, location)

    def add_item(self, item:Target, location:HasLocation):
        self.graph.add_node(item.get_id(), obj=item, type='item')
        self.__add_edge(item, location)
        if item.get_inside():
            self.add_location_detail(item.get_inside(), item)
        if item.get_on():
            self.add_location_detail(item.get_on(), item)

    def add_character(self, character:Actor, location:HasLocation):
        self.graph.add_node(character.get_id(), obj=character, type='character')
        self.__add_edge(character, location)
        if character.get_inside():
            self.add_location_detail(character.get_inside(), character)
        if character.get_on():
            self.add_location_detail(character.get_on(), character)
        self.add_location_detail(character.get_inventory(), character)
        self.add_location_detail(character.get_wearing(), character)

    # mutators

    def move(self, item:HasLocation, location:HasLocation):
        parents = self.get_parents(item)
        if not (len(parents) == 1 and parents[0].get_id() == location.get_id()):
            raise RuntimeError("Wrong number of parents for item to be moved.")
        parent = parents[0]
        self.graph.remove_edge(item.get_id(), parent.get_id())
        self.graph.remove_edge(parent.get_id(), item.get_id())
        self.graph.add_edge(location.get_id(), item.get_id(), relationship="child")
        self.graph.add_edge(item.get_id(), location.get_id(), relationship="parent")

    # utils

    def get_inventory_contents(self, character:Actor) -> list[HasLocation]:
        inventory = character.get_inventory()
        contents  = self.get_children(inventory)
        return contents

    def get_local_tree(self, item:HasLocation) -> 'ItemTree':
        ancestors   : set[str] = nx.ancestors(self.graph, item.get_id())
        descendants : set[str] = nx.descendants(self.graph, item.get_id())
        nodes                 = ancestors | {item.get_id()} | descendants
        subgraph              = self.graph.subgraph(nodes).copy()
        return subgraph

    def get_parents(self, item:HasLocation) -> list[HasLocation]:
        return [self.graph.nodes[p]['obj'] for p in self.graph.predecessors(item.get_id())]

    def get_children(self, item:HasLocation) -> list[HasLocation]:
        return [self.graph.nodes[c]['obj'] for c in self.graph.successors(item.get_id())]

    def get_weight(self, item:HasLocation) -> float:
        children = self.get_children(item)
        return sum(self.get_weight(child) for child in children) + item.get_weight()

    def get_size(self, item:HasLocation) -> float:
        children = self.get_children(item)
        return sum(self.get_size(child) for child in children) + item.get_size()

    def get_value(self, item:HasLocation) -> float:
        children = self.get_children(item)
        return sum(self.get_value(child) for child in children) + item.get_value()

    def get_weight_of_contents(self, item:HasLocation) -> float:
        return self.get_weight(item) - item.get_weight()

    def get_size_of_contents(self, item:HasLocation) -> float:
        return self.get_size(item) - item.get_size()

    def get_value_of_contents(self, item:HasLocation) -> float:
        return self.get_value(item) - item.get_value()

    def get_room(self, item:HasLocation) -> Location:
        while not isinstance(self.graph[item]["is_in"], Location):
            item = self.graph[item]["is_in"]
        return self.graph[item]["is_in"]

class WorldMap:
    def __init__(self):
        self.world_map = dict[Location,dict[Direction,Path]]()

    # initialization

    def add_path(self, path:Path):
        for start,direction in path.list_starts():
            if not start in self.world_map:
                self.world_map[start] = dict[Direction,Path]()
            self.world_map[start][direction] = path

    # utils

    def get_paths(self, room:Location) -> list[Path]:
        return list(self.world_map[room].values())

    def get_path(self, room:Location, direction:Direction) -> Path|None:
        return self.world_map[room].get(direction)

class World:

    def __init__(self):
        self.item_locations = ItemTree()
        self.world_map      = WorldMap()

    # MOVEMENT

    def walk(self, character:Actor, direction:Direction) -> tuple[bool,Description]:
        room = self.get_room(character)
        path = self.get_path(room, direction)
        if path is None:
            return False, plain_text_description("Path does not exist.")
        can_pass, response = path.can_pass(RestrictionContext(character, self.item_locations.get_local_tree(character)))
        if can_pass:
            end = path.get_end(PathEndContext(character, self.item_locations.get_local_tree(character), room))
            if end: # end should never be None but just in case
                self.item_locations.move(character, end)
                return True, response
        return False, response

    def move_item(self, item:HasLocation, new_spot:HasLocation) -> tuple[bool,Description]:
        if not self.get_room(item) == self.get_room(new_spot):
            return False, plain_text_description(f"{item.get_name()} is not in the same room as {new_spot.get_name()}")
        if can_fit(item, new_spot, self):
            self.item_locations.move(item, new_spot)
            return True, None
        return False, plain_text_description(f"There is no room in {new_spot.get_name()} for {item.get_name()}")

    # UTILS

    def get_room(self, item:HasLocation) -> Location:
        return self.item_locations.get_room(item)

    def get_path(self, room:Location, direction:Direction) -> Path|None:
        return self.world_map.get_path(room, direction)

    # DESCRIPTIONS

    def describe_room(self, room:Location, description_context:DescriptionContext, restriction_context:RestrictionContext) -> str:
        responses = [plain_text_description(f"[{room.get_name()}]"), room.describe()]

        for path in self.world_map.get_paths(room):
            if path.is_visible(restriction_context):
                responses.append(path.describe(description_context))
        for child in self.item_locations.get_children(room):
            if child.is_visible(restriction_context) and not child == RestrictionContext.character:
                if isinstance(child, Target):
                    responses.append(Description[CombinationContext](CombinationContext([plain_text_description("There is"), child.describe()], joiner=" "), CombinationDescription()))
                else:
                    responses.append(child.describe())
        return Description[CombinationContext](CombinationContext(responses), CombinationDescription())
