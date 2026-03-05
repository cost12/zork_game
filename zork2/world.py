import dataclasses
import re
import string
import logging
from abc import abstractmethod
from typing import Callable

from frozendict import frozendict

from .utils import ItemTree, WorldMap, NameFinder, ItemLimit, Named, HasInventory, HasWearing, Container, Path, HasLocation

logger = logging.getLogger(__name__)

class Visible(Named):
    @abstractmethod
    def can_interact_with(self, rules: 'WorldRules', world: 'World', other_id: str, action_id: str, inform: Callable[[str],None]) -> bool:
        pass

    @abstractmethod
    def describe(self, rules: 'WorldRules', world: 'World', character_id: str, inform: Callable[[str],None]) -> None:
        pass

@dataclasses.dataclass(frozen=True)
class NamedBase(Named):
    name : str
    aliases : tuple[str,...] = dataclasses.field(kw_only=True, default_factory=tuple)
    name_id : str = dataclasses.field(kw_only=True, default=None)

    def __post_init__(self):
        if not self.name_id:
            object.__setattr__(self, 'name_id', self.name)
        object.__setattr__(self, 'name_id', self.name_id.lower())
        if not self.aliases or len(self.aliases) == 0:
            object.__setattr__(self, 'aliases', (self.name,))
        new_aliases = [alias.lower() for alias in self.aliases]
        if self.name.lower() not in self.aliases:
            new_aliases.append(self.name.lower())
        object.__setattr__(self, 'aliases', tuple(new_aliases))

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.name_id

    def get_aliases(self) -> list[str]:
        return list(self.aliases)

@dataclasses.dataclass(frozen=True)
class VisibleBase(NamedBase, Visible):
    descriptor : Callable[[str,'WorldRules','World',str,Callable[[str],None]],None]
    interactor : Callable[[str,'WorldRules','World',str,str,Callable[[str],None]],bool]

    def can_interact_with(self, rules: 'WorldRules', world: 'World', other_id: str, action_id: str, inform: Callable[[str],None]) -> bool:
        return self.interactor(self.get_id(), rules, world, other_id, action_id, inform)

    def describe(self, rules: 'WorldRules', world: 'World', character_id: str, inform: Callable[[str],None]) -> None:
        return self.descriptor(self.get_id(), rules, world, character_id, inform)

@dataclasses.dataclass(frozen=True)
class Item(VisibleBase, HasLocation):
    weight : float = dataclasses.field(kw_only=True, default=1.0)
    size : float = dataclasses.field(kw_only=True, default=1.0)
    value : float = dataclasses.field(kw_only=True, default=0.0)

    def get_weight(self) -> float:
        return self.weight

    def get_size(self) -> float:
        return self.size

    def get_value(self) -> float:
        return self.value

@dataclasses.dataclass(frozen=True)
class ContainerItem(Item, Container):
    item_limit : ItemLimit = ItemLimit()

    def get_limit(self) -> ItemLimit:
        return self.item_limit

@dataclasses.dataclass(frozen=True)
class Character(Item, HasInventory, HasWearing):
    inventory_id : str
    wearing_id : str

    def get_children(self, names: NameFinder) -> list[HasLocation]:
        return [names.get_from_id(self.inventory_id), names.get_from_id(self.wearing_id)]

    def get_inventory(self, names: NameFinder) -> Container:
        return names.get_from_id(self.inventory_id)

    def get_wearing(self, names: NameFinder) -> Container:
        return names.get_from_id(self.wearing_id)

@dataclasses.dataclass(frozen=True)
class Room(VisibleBase, Container):
    item_limit : ItemLimit = ItemLimit()

    def get_limit(self) -> ItemLimit:
        return self.item_limit

@dataclasses.dataclass(frozen=True)
class PathWay(VisibleBase, Path):
    starts : tuple[tuple[str, str]]
    end_id : str
    item_limit : ItemLimit = ItemLimit()

    def get_limit(self) -> ItemLimit:
        return self.item_limit

    def get_end(self, names: NameFinder) -> Container:
        return names.get_from_id(self.end_id)

    def list_starts(self, names: NameFinder):
        return [
            (names.get_from_id(room), names.get_from_id(direction)) for room, direction in self.starts
        ]

    def list_possible_ends(self, names: NameFinder, start: Container) -> list[Container]:
        return [names.get_from_id(self.end_id)]

@dataclasses.dataclass(frozen=True)
class ActionEdge:
    category : str
    form : str|None = None

    def __repr__(self) -> str:
        return f"<{self.category} ({self.form})>"

    def find_match(self, character: Character, world: 'World', input_str: str) -> tuple[bool, tuple[str, str], str]:
        match self.category:
            case 'literal':
                if len(input_str) >= len(self.form) and input_str[:len(self.form)]==self.form:
                    return True, (self.form, self.form), input_str[len(self.form)+1:]
            case 'regex':
                m = re.search(f"^{self.form}", input_str, re.IGNORECASE)
                if m:
                    return True, (m.group(0), m.group(1)), input_str[len(m.group(0))+1:]
            case _:
                matches = world.find_matches(character, input_str, self.category)
                if self.form:
                    matches = [m for m in matches if isinstance(m[1], Named) and m[1].get_id() == self.form]
                if len(matches) > 0:
                    return True, (matches[0][0], matches[0][1].get_id()), matches[0][2]
        return False, ("", ""), input_str

@dataclasses.dataclass(frozen=True)
class ActionInput:
    name : str
    edge : ActionEdge

    def get_name(self) -> str:
        return self.name

    def get_edge(self) -> ActionEdge:
        return self.edge

    def get_defaults(self) -> dict[str, Named]:
        return {}

@dataclasses.dataclass(frozen=True)
class Action(NamedBase):
    forms : tuple[tuple[ActionInput,...]]
    actor : Callable[[str,'WorldRules','World',str,dict[str,str],Callable[[str],None]],tuple[bool,'World']]

    def get_input_forms(self) -> tuple[tuple[ActionInput]]:
        return self.forms

    def perform_action(self, rules: 'WorldRules', world: 'World', character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> tuple[bool,'World']:
        return self.actor(self.get_id(), rules, world, character_id, inputs, inform)

    def get_inputs(self, form_inputs: tuple[tuple[ActionEdge, Named]]) -> dict[str, Named]:
        for form in self.forms:
            out = {}
            if len(form) != len(form_inputs):
                continue
            found_match = True
            for i, action_input in enumerate(form):
                if action_input.get_edge() == form_inputs[i][0]:
                    out = out | action_input.get_defaults()
                    out[action_input.get_name()] = form_inputs[i][1]
                else:
                    found_match = False
                    break
            if found_match:
                out.pop('self', None)
                return out
        return {}

class ParseNode:
    def __init__(self, value: frozenset[str]|None = None, children: frozendict[ActionEdge, 'ParseNode']|None = None):
        self.__value : frozenset[str] = value if value else frozenset()
        self.__children : frozendict[ActionEdge, ParseNode] = children if children else frozendict()

    def get_rep(self, previous: str) -> str:
        rep = f"{previous}: {set(self.__value)}"
        for edge, child in self.__children.items():
            rep += f"\n{child.get_rep(previous + " " + str(edge))}"
        return rep

    def add_action_form(self, action: Action, form: tuple[ActionInput]) -> 'ParseNode':
        new_value = set(self.__value)
        new_children = dict(self.__children)
        if len(form) == 0:
            new_value = new_value.union([action.get_id()])
        else:
            edge = form[0].get_edge()
            if edge in new_children:
                new_children[edge] = new_children[edge].add_action_form(action, form[1:])
            else:
                new_children[edge] = ParseNode().add_action_form(action, form[1:])
        return ParseNode(frozenset(new_value), frozendict(new_children))

    def add_action(self, action: Action) -> 'ParseNode':
        node = self
        for form in action.get_input_forms():
            node = node.add_action_form(action, form)
        return node

    def continue_parse(self, character: Character, world: 'World', input_str: str, already_found: tuple[str]) -> tuple[str, dict[str, str]]:
        if len(input_str) == 0:
            return tuple((action, world.get_action(action).get_inputs(already_found)) for action in self.__value)
        matches = []
        for edge, node in self.__children.items():
            matched, found, left = edge.find_match(character, world, input_str)
            if matched:
                matches.extend(node.continue_parse(character, world, left, already_found + ((edge, found[1]),)))
        return tuple(matches)

    def parse_input(self, character: Character, world: 'World', input_str: str) -> tuple[tuple[str, dict[str, str]]]:
        input_str = re.sub(r"\b(a|an|the|i)\b", "", input_str, flags=re.IGNORECASE)
        punctuation = "|".join(re.escape(c) for c in string.punctuation)
        input_str = re.sub(rf"{punctuation}", "", input_str)
        input_str = re.sub(r"\s+", " ", input_str)
        input_str = re.sub(r"^\s+", "", input_str)
        input_str = re.sub(r"\s+$", "", input_str)
        if len(input_str) == 0:
            return tuple((action, world.get_action(action).get_inputs(tuple())) for action in self.__value)
        matches = []
        for edge, node in self.__children.items():
            matched, found, left = edge.find_match(character, world, input_str)
            if matched:
                matches.extend(node.continue_parse(character, world, left, ((edge, found[1]),)))
        return tuple(matches)

@dataclasses.dataclass(frozen=True)
class ActionLogLine:
    character_id : str
    room_id : str
    action_id : str
    success : bool
    score : int = 0

class ActionLog:
    def __init__(self, actions: tuple[ActionLogLine]|None=None):
        self.__actions : tuple[ActionLogLine] = actions if actions else tuple()

    def __repr__(self):
        return str(self.__actions)

    def update_log(self, log_line: ActionLogLine) -> 'ActionLog':
        return ActionLog(self.__actions + (log_line,))

    def action_count(self, character_id: str|None=None, room_id: str|None=None, action_id: str|None=None, success: bool|None=None) -> int:
        return len([
            action for action in self.__actions if
                (action.character_id == character_id or character_id is None) and \
                (action.room_id      == room_id      or room_id is None) and \
                (action.action_id    == action_id    or action_id is None) and \
                (action.success      == success      or success is None)
        ])

    def action_score(self, character_id: str|None=None, room_id: str|None=None, action_id: str|None=None, success: bool|None=None) -> int:
        return sum(
            action.score for action in self.__actions if
                (action.character_id == character_id or character_id is None) and \
                (action.room_id      == room_id      or room_id is None) and \
                (action.action_id    == action_id    or action_id is None) and \
                (action.success      == success      or success is None)
        )

class World:

    def __init__(self, *, init_locations: ItemTree|None=None, init_map: WorldMap|None=None, init_names: NameFinder|None = None, init_log: ActionLog|None = None):
        self.__item_locations = ItemTree()   if init_locations is None else init_locations
        self.__world_map      = WorldMap()   if init_map       is None else init_map
        self.__names          = NameFinder() if init_names     is None else init_names
        self.__log            = ActionLog()  if init_log       is None else init_log

    def __repr__(self) -> str:
        rep =  f"\nItems: {self.__item_locations}"
        rep += f"\nMap: {self.__world_map.get_rep(self.__names)}"
        rep += f"\nNames: {self.__names}"
        rep += f"\nLog: {self.__log}"
        return rep

    def __update(self, *, new_locations: ItemTree|None=None, new_map: WorldMap|None=None, new_names: NameFinder|None=None, new_log: ActionLog|None=None) -> 'World':
        return World(
            init_locations=new_locations if new_locations else self.__item_locations,
            init_map=new_map if new_map else self.__world_map,
            init_names=new_names if new_names else self.__names,
            init_log=new_log if new_log else self.__log
        )

    # init
    def add_character(self, character: Character, location: Room) -> 'World':
        new_locations = self.__item_locations.add_carrier(character, location)
        new_names = self.__names.add(character, category='character')
        return self.__update(new_locations=new_locations, new_names=new_names)

    # UTILS
    def find_matches(self, character: Character, input_str: str, category: str) -> list[tuple[str, Named, str]]:
        trees = None
        if category not in ['direction', 'action']:
            trees = []
            node = character
            while node is not None:
                trees.append(self.__item_locations.get_subtree(node))
                next_node_id = self.__item_locations.get_parent()
                if next_node_id is None:
                    node = None
                else:
                    node = self.__names.get_from_id(next_node_id)
        matches = self.__names.get_from_input(input_str.split(), category, trees)
        return [(" ".join(used), found, " ".join(left)) for found, used, left in matches]

    def get_character(self, character_id: str) -> Character:
        return self.__names.get_from_id(character_id, 'character')

    def get_visible(self, visible_id: str) -> Visible:
        return self.__names.get_from_id(visible_id)

    def get_action(self, action_id: str) -> Action:
        return self.__names.get_from_id(action_id, 'action')

    def get_room(self, item: HasLocation) -> Room:
        return self.__names.get_from_id(self.__item_locations.get_top_parent(item))

    def get_path(self, room: Room, direction: Named) -> PathWay|None:
        path = self.__world_map.get_path(room, direction)
        if path:
            return self.__names.get_from_id(path)
        return path

    def get_subtree(self, item: HasLocation) -> ItemTree:
        return self.__item_locations.get_subtree(item)

    def get_parent(self, item: HasLocation|Container) -> Container|None:
        p = self.__item_locations.get_parent(item)
        return self.__names.get_from_id(p) if p else p

    def get_locations(self) -> ItemTree:
        return self.__item_locations

    def get_log(self) -> ActionLog:
        return self.__log

    # MUTATE

    def update_log(self, log_line: ActionLogLine) -> 'World':
        new_log = self.__log.update_log(log_line)
        return self.__update(new_log=new_log)

    def walk(self, character: Character, direction: Named) -> tuple['World', bool]:
        room = self.get_room(character)
        path = self.get_path(room, direction)
        if path is None:
            return self, False
        end = path.get_end(self.__names)
        if end: # end should never be None but just in case
            new_locations = self.__item_locations.move(character, end)
            return self.__update(new_locations=new_locations), True
        return self, False

    def move_item(self, item: Item, new_spot: HasLocation) -> tuple['World', bool]:
        if not self.get_room(item) == self.get_room(new_spot):
            return self, False
        new_locations = self.__item_locations.move(item, new_spot)
        return self.__update(new_locations=new_locations), True

class WorldRules:
    def __init__(self, parser: ParseNode|None = None, actions: tuple[Action]|None = None):
        self.__parser = parser if parser else ParseNode()
        self.__actions = actions if actions else tuple()

    def __repr__(self) -> str:
        return f"\nInputs:\n{self.__parser.get_rep('\t')}"

    def add_actions(self, actions: list[Action]) -> 'WorldRules':
        new_parser = self.__parser
        for action in actions:
            new_parser = new_parser.add_action(action)
        return WorldRules(new_parser, self.__actions + tuple(actions))

    def parse_input(self, character: Character, world: World, input_str: str) -> tuple[tuple[str, dict[str, str]]]:
        return self.__parser.parse_input(character, world, input_str)

    def get_actions(self) -> list[Action]:
        return list(self.__actions)

    def advance(self, world: World, character_id: str, action_id: str, action_args: dict[str, Named], inform: Callable[[str],None]) -> tuple[bool, World]:
        logger.debug("%s: %s", action_id, action_args)
        return world.get_action(action_id).perform_action(self, world, character_id, action_args, inform)
