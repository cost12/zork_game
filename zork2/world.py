import dataclasses


from .utils import ItemTree, WorldMap, NameFinder, ItemLimit, Named, HasInventory, HasWearing, Container, Path, HasLocation

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

dataclasses.dataclass(frozen=True)
class Item(NamedBase, HasLocation):
    weight : float = 1.0
    size : float = 1.0
    value : float = 0.0

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
class Room(NamedBase, Container):
    item_limit : ItemLimit = ItemLimit()

    def get_limit(self) -> ItemLimit:
        return self.item_limit

@dataclasses.dataclass(frozen=True)
class PathWay(NamedBase, Path):
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

class World:

    def __init__(self, *, init_locations: ItemTree|None=None, init_map: WorldMap|None=None, init_names: NameFinder|None = None):
        self.__item_locations = ItemTree()   if init_locations is None else init_locations
        self.__world_map      = WorldMap()   if init_map       is None else init_map
        self.__names          = NameFinder() if init_names     is None else init_names

    # init
    def add_character(self, character: Character, location: Room) -> 'World':
        new_locations = self.__item_locations.add_carrier(character, location)
        return World(init_locations=new_locations, init_map=self.__world_map)

    # UTILS

    def get_room(self, item: HasLocation) -> Room:
        return self.__names.get_from_id(self.__item_locations.get_top_parent(item))

    def get_path(self, room: Room, direction: Named) -> PathWay|None:
        path = self.__world_map.get_path(room, direction)
        if path:
            return self.__names.get_from_id(path)
        return path

    def get_subtree(self, item: HasLocation) -> ItemTree:
        return self.__item_locations.get_subtree(item)

    def get_locations(self) -> ItemTree:
        return self.__item_locations

    # MOVEMENT

    def walk(self, character: Character, direction: Named) -> tuple['World', bool]:
        room = self.get_room(character)
        path = self.get_path(room, direction)
        if path is None:
            return self, False
        end = path.get_end(self.__names)
        if end: # end should never be None but just in case
            new_locations = self.__item_locations.move(character, end)
            return World(init_locations=new_locations, init_map=self.__world_map), True
        return self, False

    def move_item(self, item: Item, new_spot: HasLocation) -> tuple['World', bool]:
        if not self.get_room(item) == self.get_room(new_spot):
            return self, False
        new_locations = self.__item_locations.move(item, new_spot)
        return World(init_locations=new_locations, init_map=self.__world_map), True
