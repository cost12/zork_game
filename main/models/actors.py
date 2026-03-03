from typing      import TypeVar, Any
from dataclasses import dataclass, field
import random

import networkx  as nx
from frozendict import frozendict

from models.state               import State, Skill, FullState, SkillSet, Achievement
from models.named               import Named, Action, Direction
from readin.restriction_helpers import Restriction, RestrictionContext
from readin.description_helpers import Description, DescriptionStrategy, DescriptionContext, CombinationDescription, CombinationContext, plain_text_description, combine_descriptions, BackupDescription, PlainTextContext, PlainTextDescription

T = TypeVar('T')

def can_fit(item:'Container', container:'Container', item_tree:'ItemTree') -> bool:
    limit = container.get_item_limit()
    if     (limit.weight_limit is None or item_tree.get_weight(item) + item_tree.get_weight_of_contents(container) <= limit.weight_limit) \
        or (limit.size_limit   is None or item_tree.get_size(item)   + item_tree.get_size_of_contents(container)   <= limit.size_limit) \
        or (limit.value_limit  is None or item_tree.get_value(item)  + item_tree.get_value_of_contents(container)  <= limit.value_limit):
        return all(can_fit(item, c, item_tree) for c in item_tree.get_parents(container))
    return False

@dataclass(frozen=True)
class ItemLimit:
    size_limit   : float|None = None
    weight_limit : float|None = None
    value_limit  : float|None = None

@dataclass(frozen=True)
class Visible:
    description_context  : Any                    = field(default_factory=lambda: PlainTextContext("No description"))
    description_strategy : DescriptionStrategy    = field(default_factory=PlainTextDescription)
    hidden               : bool                   = False
    visible_restrictions : tuple[Restriction,...] = field(default_factory=tuple)

    def __post_init__(self):
        if not isinstance(self.visible_restrictions, tuple):
            object.__setattr__(self, 'visible_restrictions', tuple(self.visible_restrictions))

    def is_visible(self, context:RestrictionContext) -> tuple[bool,Description]:
        for visible_restriction in self.visible_restrictions:
            passes, response = visible_restriction.passes(context)
            if not passes:
                return passes, response
        return False, None

    def describe(self, context:RestrictionContext) -> Description|None:
        visible, desc =  self.is_visible(context)
        if visible:
            return Description(self, self.description_strategy, self.description_context)
        return desc

@dataclass(frozen=True)
class Container(Visible):
    item_limit     : ItemLimit                   = field(default_factory=ItemLimit)
    item_responses : frozendict['Container',str] = field(default_factory=frozendict)
    weight         : float                       = 1.0
    size           : float                       = 1.0
    value          : float                       = 0.0

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.item_responses, frozendict):
            object.__setattr__(self, 'item_responses', frozendict(self.item_responses))

    def get_weight(self) -> float:
        return self.weight

    def get_value(self) -> float:
        return self.value

    def get_size(self) -> float:
        return self.size

    def get_item_limit(self) -> ItemLimit:
        return self.item_limit

@dataclass(frozen=True)
class NamedContainer(Container, Named):
    def __post_init__(self):
        Named.__post_init__(self)
        Container.__post_init__(self)

class LocationDetail(NamedContainer):

    def __repr__(self):
        return f"<LocationDetail {self.get_name()}>"

@dataclass(frozen=True)
class PathInfo:
    start                : 'Location'
    end                  : 'Location'
    direction            : Direction
    passing_restrictions : tuple[Restriction] = field(default_factory=tuple)
    exit_response        : Description       = None
    hidden_when_locked   : bool              = False

    def __post_init__(self):
        if not isinstance(self.passing_restrictions, tuple):
            object.__setattr__(self, 'passing_restrictions', tuple(self.passing_restrictions))

@dataclass(frozen=True)
class PathEndContext:
    character      : 'Actor'
    item_locations : 'ItemTree'

@dataclass(frozen=True)
class Path(NamedContainer):
    path_info : PathInfo = field(kw_only=True)

    def __repr__(self):
        return f"<Path {self.get_name()}>"

    def is_visible(self, context):
        hidden, response = super().is_visible(context)
        if hidden:
            return hidden, response
        can_pass, pass_response = self.can_pass(context)
        if self.path_info.hidden_when_locked and not can_pass:
            return False, pass_response
        return hidden, response

    def get_direction(self) -> Direction:
        return self.path_info.direction

    def get_start(self) -> 'Location':
        return self.path_info.start

    def list_starts(self) -> list[tuple['Location',Direction]]:
        return [(self.path_info.start, self.path_info.direction)]

    def get_end(self, context:PathEndContext) -> 'Location|None':
        return self.path_info.end

    def can_pass(self, context:RestrictionContext) -> tuple[bool,Description]:
        for restriction in self.path_info.passing_restrictions:
            passes, response = restriction.passes(context)
            if not passes:
                return passes, response
        return True, None

@dataclass(frozen=True)
class TwoWayPath(Path):
    reverse_direction : Direction = field(kw_only=True)
    reverse_description_context : DescriptionContext = field(kw_only=True)
    reverse_description_strategy : DescriptionStrategy = field(kw_only=True)
    reverse_passing_restrictions : tuple[Restriction] = field(kw_only=True, default_factory=tuple)

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.reverse_passing_restrictions, tuple):
            object.__setattr__(self, 'reverse_passing_restrictions', tuple(self.reverse_passing_restrictions))

    def describe(self, context):
        if context.inventory.get_room(context.character) == self.path_info.start:
            return super().describe(context)
        visible, desc = self.is_visible(context)
        if visible:
            return Description(self, self.reverse_description_strategy, self.reverse_description_context)
        return desc

    def list_starts(self) -> list[tuple['Location',Direction]]:
        return [(self.path_info.start,self.path_info.direction), (self.path_info.end,self.reverse_direction)]

    def get_end(self, context:PathEndContext) -> 'Location|None':
        if context.item_locations.get_room(context.character) == self.path_info.start:
            return self.path_info.end
        return self.path_info.start

    def can_pass(self, context:RestrictionContext) -> tuple[bool,Description]:
        if context.inventory.get_room(context.character) == self.path_info.start:
            return super().can_pass(context)
        for restriction in self.reverse_passing_restrictions:
            passes, response = restriction.passes(context)
            if not passes:
                return passes, response
        return True, None

@dataclass(frozen=True)
class MultiPath(Path):
    multi_end : frozendict['Target','Location'] = field(kw_only=True)

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.multi_end, frozendict):
            object.__setattr__(self, 'multi_end', frozendict(self.multi_end))

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

    def get_end(self, context:PathEndContext) -> 'Location|None':
        inventory = context.item_locations.get_inventory_contents(context.character)
        overlap   = [item for item in inventory if item in self.multi_end]
        if len(overlap) == 0:
            return self.path_info.end
        if len(overlap) == 1:
            return overlap[0]
        return None

@dataclass(frozen=True)
class TargetInfo:
    states           : FullState
    target_responses : frozendict[Action,Description] = field(default_factory=frozendict)
    tool_responses   : frozendict[Action,Description] = field(default_factory=frozendict)
    state_responses  : frozendict[State, Description] = field(default_factory=frozendict)
    inside           : LocationDetail|None      = None
    on               : LocationDetail|None      = None

    def __post_init__(self):
        if not isinstance(self.target_responses, frozendict):
            object.__setattr__(self, 'target_responses', frozendict(self.target_responses))
        if not isinstance(self.tool_responses, frozendict):
            object.__setattr__(self, 'tool_responses', frozendict(self.tool_responses))
        if not isinstance(self.state_responses, frozendict):
            object.__setattr__(self, 'state_responses', frozendict(self.state_responses))

@dataclass(frozen=True)
class Target(NamedContainer):
    target_info : TargetInfo = field(kw_only=True)

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
        return Description[CombinationContext](self, CombinationContext(response), CombinationDescription())

    def perform_action_as_tool(self, action:Action) -> Description:
        response = list[Description]()
        new_states = self.target_info.states.perform_action_as_tool(action)
        for new_state in new_states:
            if new_state in self.target_info.state_responses:
                response.append(self.target_info.state_responses[new_state])
        return Description[CombinationContext](self, CombinationContext(response), CombinationContext)

@dataclass(frozen=True)
class ActorInfo:
    skills          : SkillSet
    inventory       : LocationDetail
    wearing         : LocationDetail
    achievements    : frozenset[Achievement]         = field(default_factory=frozenset)
    actor_responses : frozendict[Action,Description] = field(default_factory=frozendict)
    actor_type      : str                            = 'Standard'

    def __post_init__(self):
        if not isinstance(self.achievements, frozenset):
            object.__setattr__(self, 'achievements', frozenset(self.achievements))
        if not isinstance(self.actor_responses, frozendict):
            object.__setattr__(self, 'actor_responses', frozendict(self.actor_responses))

@dataclass(frozen=True)
class Actor(Target):
    actor_info : ActorInfo = field(kw_only=True)

    def __repr__(self):
        return f"<Actor {self.get_name()}>"

    # initializers

    def _set_inventory(self, inventory: LocationDetail):
        object.__setattr__(self.actor_info, 'inventory', inventory)

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
        return Description[CombinationContext](self, CombinationContext(response), CombinationDescription())

    # ACHIEVEMENTS

    def has_completed_achievement(self, achievement:Achievement) -> bool:
        return achievement in self.actor_info.achievements

    def complete_achievement(self, achievement:Achievement) -> None:
        self.actor_info.achievements.add(achievement)

@dataclass(frozen=True)
class LocationInfo:
    is_start_location   : bool                           = False
    action_restrictions : frozendict[Action,list[Restriction]] = field(default_factory=frozendict)
    direction_responses : frozendict[Direction,Description]    = field(default_factory=frozendict)

    def __post_init__(self):
        if not isinstance(self.action_restrictions, frozendict):
            object.__setattr__(self, 'action_restrictions', frozendict(self.action_restrictions))
        if not isinstance(self.direction_responses, frozendict):
            object.__setattr__(self, 'direction_responses', frozendict(self.direction_responses))

@dataclass(frozen=True)
class Location(NamedContainer):
    location_info : LocationInfo = field(kw_only=True)

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

# TODO: state tracker for targets/actors - some sort of dict[Target,State] so targets remain immutable but can have state updates
# TODO: probably similar skill/achievement trackers for actors - dict[Actor, Skill] / dict[Actor, Achievement]
# TODO: inventory/wearing size should be stored in Actor - create inventory automatically in ItemTree
# TODO: figure out a way around StandIn
# TODO: there are still items left to be placed in other items - scan data/items to find

class ItemTree:
    def __init__(self, *, graph:nx.DiGraph=None):
        self.__graph = graph if graph else nx.DiGraph()

    # initialization

    def add_room(self, room:Location) -> 'ItemTree':
        new_graph = self.__graph.copy()
        new_graph.add_node(room.get_id(), obj=room, type="room")
        return ItemTree(graph=new_graph)

    def add_path(self, path:Path) -> 'ItemTree':
        new_graph = self.__graph.copy()
        new_graph.add_node(path.get_id(), obj=path, type='path')
        return ItemTree(graph=new_graph)

    def __add_edge(self, graph: nx.DiGraph, child:NamedContainer, parent:NamedContainer):
        graph.add_edge(parent.get_id(), child.get_id(), relationship="child")

    def __add_location_detail(self, graph: nx.DiGraph, location_detail:LocationDetail, location:NamedContainer):
        graph.add_node(location_detail.get_id(), obj=location_detail, type='location_detail')
        self.__add_edge(graph, location_detail, location)

    def add_location_detail(self, location_detail:LocationDetail, location:NamedContainer) -> 'ItemTree':
        new_graph = self.__graph.copy()
        self.__add_location_detail(new_graph, location_detail, location)
        return ItemTree(graph=new_graph)

    def add_item(self, item:Target, location:NamedContainer) -> 'ItemTree':
        new_graph = self.__graph.copy()
        new_graph.add_node(item.get_id(), obj=item, type='item')
        self.__add_edge(new_graph, item, location)
        if item.get_inside():
            self.__add_location_detail(new_graph, item.get_inside(), item)
        if item.get_on():
            self.__add_location_detail(new_graph, item.get_on(), item)
        return ItemTree(graph=new_graph)

    def add_character(self, character:Actor, location:NamedContainer) -> 'ItemTree':
        new_graph = self.__graph.copy()
        new_graph.add_node(character.get_id(), obj=character, type='character')
        self.__add_edge(new_graph, character, location)
        if character.get_inside():
            self.__add_location_detail(new_graph, character.get_inside(), character)
        if character.get_on():
            self.__add_location_detail(new_graph, character.get_on(), character)
        self.__add_location_detail(new_graph, character.get_inventory(), character)
        self.__add_location_detail(new_graph, character.get_wearing(), character)
        return ItemTree(graph=new_graph)

    # mutators

    def move(self, item:NamedContainer, location:NamedContainer) -> 'ItemTree':
        new_graph = self.__graph.copy()
        parents = self.get_parents(item)
        if not (len(parents) == 1 and parents[0].get_id() == location.get_id()):
            raise RuntimeError("Wrong number of parents for item to be moved.")
        parent = parents[0]
        new_graph.remove_edge(parent.get_id(), item.get_id())
        new_graph.add_edge(location.get_id(), item.get_id(), relationship="child")
        return ItemTree(graph=new_graph)

    # utils

    def get_inventory_contents(self, character:Actor) -> list[NamedContainer]:
        inventory = character.get_inventory()
        contents  = self.get_children(inventory)
        return contents

    def is_wearing(self, character:Actor, item:Target) -> bool:
        return item in self.get_children(character.get_wearing())

    def is_holding(self, character:Actor, item:Target) -> bool:
        return item in self.get_children(character.get_inventory())

    def get_local_tree(self, item:NamedContainer) -> 'ItemTree':
        ancestors   : set[str] = nx.ancestors(self.__graph, item.get_id())
        descendants : set[str] = nx.descendants(self.__graph, item.get_id())
        nodes                  = ancestors | {item.get_id()} | descendants
        subgraph               = self.__graph.subgraph(nodes).copy()
        return ItemTree(graph=subgraph)

    def get_parents(self, item:NamedContainer) -> list[NamedContainer]:
        return [self.__graph.nodes[p]['obj'] for p in self.__graph.predecessors(item.get_id())]

    def get_children(self, item:NamedContainer) -> list[NamedContainer]:
        return [self.__graph.nodes[c]['obj'] for c in self.__graph.successors(item.get_id())]

    def get_weight(self, item:NamedContainer) -> float:
        children = self.get_children(item)
        return sum(self.get_weight(child) for child in children) + item.get_weight()

    def get_size(self, item:NamedContainer) -> float:
        children = self.get_children(item)
        return sum(self.get_size(child) for child in children) + item.get_size()

    def get_value(self, item:NamedContainer) -> float:
        children = self.get_children(item)
        return sum(self.get_value(child) for child in children) + item.get_value()

    def get_weight_of_contents(self, item:NamedContainer) -> float:
        return self.get_weight(item) - item.get_weight()

    def get_size_of_contents(self, item:NamedContainer) -> float:
        return self.get_size(item) - item.get_size()

    def get_value_of_contents(self, item:NamedContainer) -> float:
        return self.get_value(item) - item.get_value()

    def get_room(self, item:NamedContainer) -> Location|Path:
        top = item
        parents = list(self.__graph.predecessors(item))
        while parents:
            top = parents[0]
            parents = list(self.__graph.predecessors(parents[0]))
        return top

class WorldMap:
    def __init__(self, *, init_map: frozendict[Location,frozendict[Direction,Path]]|None=None):
        self.__world_map : frozendict[Location,frozendict[Direction,Path]] = init_map if init_map is not None else frozendict()

    # initialization

    def add_path(self, path:Path) -> 'WorldMap':
        new_map = {key:dict(val) for key, val in self.__world_map.items()}
        for start, direction in path.list_starts():
            if not start in new_map:
                new_map[start] = {}
            new_map[start][direction] = path
        return WorldMap(init_map=frozendict({key:frozendict(val) for key, val in new_map.items()}))

    # utils

    def are_adjacent(self, location:Location, path:Path) -> int:
        return path in self.__world_map[location].values()

    def get_paths(self, room:Location) -> list[Path]:
        return list(self.__world_map[room].values())

    def get_path(self, room:Location, direction:Direction) -> Path|None:
        if direction.get_name() == "random":
            return random.choice(list(self.__world_map[room].values()))
        return self.__world_map[room].get(direction)

class World:

    def __init__(self, *, init_locations: ItemTree|None=None, init_map: WorldMap|None=None):
        self.__item_locations = ItemTree() if init_locations is None else init_locations
        self.__world_map      = WorldMap() if init_map       is None else init_map

    # init
    def add_character(self, character: Actor, location: Location) -> 'World':
        new_locations = self.__item_locations.add_character(character, location)
        return World(init_locations=new_locations, init_map=self.__world_map)

    # MOVEMENT

    def walk(self, character:Actor, direction:Direction) -> tuple['World',bool,Description]:
        room = self.get_room(character)
        path = self.get_path(room, direction)
        if path is None:
            return False, plain_text_description(f"There is no path to the {direction.get_name()}.")
        can_pass, response = path.can_pass(RestrictionContext(character, self.__item_locations.get_local_tree(character)))
        if can_pass:
            end = path.get_end(PathEndContext(character, self.__item_locations.get_local_tree(character)))
            if end: # end should never be None but just in case
                new_locations = self.__item_locations.move(character, end)
                return World(init_locations=new_locations, init_map=self.__world_map), True, response
        return self, False, response

    def move_item(self, item:NamedContainer, new_spot:NamedContainer) -> tuple['World',bool,Description]:
        if not self.get_room(item) == self.get_room(new_spot):
            return False, plain_text_description(f"{item.get_name()} is not in the same room as {new_spot.get_name()}")
        if can_fit(item, new_spot, self):
            new_locations = self.__item_locations.move(item, new_spot)
            return World(init_locations=new_locations, init_map=self.__world_map), True, None
        return self, False, plain_text_description(f"There is no room in {new_spot.get_name()} for {item.get_name()}")

    # UTILS

    def get_room(self, item:NamedContainer) -> Location:
        return self.__item_locations.get_room(item)

    def get_path(self, room:Location, direction:Direction) -> Path|None:
        return self.__world_map.get_path(room, direction)

    def get_local_tree(self, item:NamedContainer) -> ItemTree:
        return self.__item_locations.get_local_tree(item)

    def get_locations(self) -> ItemTree:
        return self.__item_locations

    # ACTIONS

    def can_interact(self, character:Actor, item:NamedContainer) -> bool:
        if not item.is_visible(RestrictionContext(character, self.__item_locations.get_local_tree(character))):
            return False
        room = self.__item_locations.get_room(character)
        item_room = self.__item_locations.get_room(item)
        if not (room == item_room or self.__world_map.are_adjacent(room, item_room)):
            return False
        return True

    def can_act_on(self, character:Actor, target:Target, action:Action) -> tuple[bool,Description]:
        # room
        room = self.__item_locations.get_room(character)
        allowed, room_desc = room.action_allowed(RestrictionContext(character, self.__item_locations.get_local_tree(character)))
        if not allowed:
            return False, room_desc
        # access items
        if not self.can_interact(character, target):
            return False, plain_text_description(f"You can't see a {target.get_name()} here.")
        # character
        character_desc = character.get_actor_response(action)
        if not action in character.get_actions_as_actor():
            character_desc = Description[list[Description]](
                character,
                [
                    character_desc,
                    plain_text_description(f"Try as you might, you seem physically incapable of {action.get_name()}.")
                ],
                BackupDescription()
            )
            return False, combine_descriptions([room_desc, character_desc])
        # items
        target_desc = target.get_target_response(action)
        if not action in target.get_actions_as_target():
            target_desc = Description[list[Description]](
                target,
                [
                    target_desc,
                    plain_text_description(f"Unfortunately you can {action.get_name()} the {target.get_name()}.")
                ],
                BackupDescription()
            )
            return False, combine_descriptions([room_desc, character_desc, target_desc])
        # success
        return True, combine_descriptions([room_desc, character_desc, target_desc])

    def can_use(self, character:Actor, tool:Target, action:Action) -> bool:
        # room
        room = self.__item_locations.get_room(character)
        allowed, room_desc = room.action_allowed(RestrictionContext(character, self.__item_locations.get_local_tree(character)))
        if not allowed:
            return False, room_desc
        # access items
        if not self.can_interact(character, tool):
            return False, plain_text_description(f"You can't see a {tool.get_name()} here.")
        # character
        character_desc = character.get_actor_response(action)
        if not action in character.get_actions_as_actor():
            character_desc = Description[list[Description]](
                character,
                [
                    character_desc,
                    plain_text_description(f"Try as you might, you seem physically incapable of {action.get_name()}.")
                ],
                BackupDescription()
            )
            return False, combine_descriptions([room_desc, character_desc])
        # items
        tool_desc = tool.get_tool_response(action)
        if not action in tool.get_actions_as_tool():
            tool_desc = Description[list[Description]](
                tool,
                [
                    tool_desc,
                    plain_text_description(f"Unfortunately you can {action.get_name()} with a {tool.get_name()}.")
                ],
                BackupDescription()
            )
            return False, combine_descriptions([room_desc, character_desc, tool_desc])
        # success
        return True, combine_descriptions([room_desc, character_desc, tool_desc])

    def can_act(self, character:Actor, action:Action) -> bool:
        # room
        room = self.__item_locations.get_room(character)
        allowed, room_desc = room.action_allowed(RestrictionContext(character, self.__item_locations.get_local_tree(character)))
        if not allowed:
            return False, room_desc
        # character
        character_desc = character.get_actor_response(action)
        if not action in character.get_actions_as_actor():
            character_desc = Description[list[Description]](
                character,
                [
                    character_desc,
                    plain_text_description(f"Try as you might, you seem physically incapable of {action.get_name()}.")
                ],
                BackupDescription()
            )
            return False, combine_descriptions([room_desc, character_desc])
        # success
        return True, combine_descriptions([room_desc, character_desc])

    # DESCRIPTIONS

    def describe_room(self, room:Location, restriction_context:RestrictionContext) -> Description:
        responses = [plain_text_description(f"[{room.get_name()}]"), room.describe(restriction_context)]

        for path in self.__world_map.get_paths(room):
            if path.is_visible(restriction_context):
                responses.append(path.describe(restriction_context))
        for child in self.__item_locations.get_children(room):
            if child.is_visible(restriction_context) and not child == RestrictionContext.character:
                if isinstance(child, Target):
                    responses.append(combine_descriptions([plain_text_description("There is"), child.describe(restriction_context)], joiner=" "))
                else:
                    responses.append(child.describe(restriction_context))
        return combine_descriptions(responses)
