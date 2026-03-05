import logging

from zork2.world import World, WorldRules, Character, Item, ContainerItem, Room, PathWay, NamedBase, Action, ActionInput, ActionEdge
from zork2.utils import Named, NameFinder, ItemTree, WorldMap

from zork2.descriptions import plain_text, room_description, path_description
from zork2.interactions import simple_interaction
from zork2.actions import look, walk, bad_input, debug

logger = logging.getLogger(__name__)

def load_directions() -> list[Named]:
    return [
        NamedBase("north", aliases=['n']),
        NamedBase("south", aliases=['s']),
    ]

def load_characters() -> list[Character]:
    return [
        Character(
            "Player1",
            descriptor=plain_text("A handsome fellow.", 'a handsome fellow'),
            interactor=simple_interaction(),
            inventory_id="player1 inventory",
            wearing_id="player1 wearing",
        ),
    ]

def load_items() -> list[Item]:
    return [
        ContainerItem(
            "player1 inventory",
            descriptor=plain_text("An inventory.", 'an inventory'),
            interactor=simple_interaction(),
        ),
        ContainerItem(
            "player1 wearing",
            descriptor=plain_text("", ''),
            interactor=simple_interaction(),
        ),
    ]

def load_rooms() -> list[Room]:
    return [
        Room(
            "Grey Room",
            descriptor=room_description("You are standing in a grey room, with a view...", "In the room sits"),
            interactor=simple_interaction(),
        ),
        Room(
            "Gray Room",
            descriptor=room_description("You see a gray room, with a view...", "In the room you find"),
            interactor=simple_interaction(),
        ),
    ]

def load_paths() -> list[PathWay]:
    return [
        PathWay(
            "Gray South exit",
            descriptor=path_description("A musty passage way.", 'A gray path stretches {direction}.', "In the path, you find"),
            interactor=simple_interaction(),
            starts=(("gray room", "south"),),
            end_id="grey room",
        ),
        PathWay(
            "Grey North exit",
            descriptor=path_description("A musty passage way.", 'A grey path winds {direction}.', "In the path, you find"),
            interactor=simple_interaction(),
            starts=(("grey room", "north"),),
            end_id="gray room",
        ),
    ]

def load_actions():
    return [
        Action(
            'bad input',
            (tuple(),),
            bad_input(),
        ),
        Action(
            'debug',
            ((ActionInput('self', ActionEdge('action', 'debug')),),),
            debug(),
        ),
        Action(
            'walk',
            (
                (
                    ActionInput('direction', ActionEdge('direction')),
                ),
                (
                    ActionInput('self', ActionEdge('action', 'walk')),
                    ActionInput('direction', ActionEdge('direction')),
                ),
            ),
            walk(),
            aliases=['go']
        ),
        Action(
            'look',
            (
                (ActionInput('self', ActionEdge('action', 'look')),),
            ),
            look(),
        )
    ]

def load_start_locations(names: NameFinder, locations: ItemTree) -> ItemTree:
    return locations.add_carrier(names, names.get_from_id('player1'), names.get_from_id('gray room'), 'character', 'inventory')

def load_world() -> tuple[WorldRules, World]:
    locations = ItemTree()
    world_map = WorldMap()
    names = NameFinder()

    directions = load_directions()
    actions = load_actions()
    characters = load_characters()
    items = load_items()
    rooms = load_rooms()
    paths = load_paths()

    added, names = names.add_many(directions, category='direction')
    logger.debug(added)
    added, names = names.add_many(actions, category='action')
    logger.debug(added)
    added, names = names.add_many(characters, category='character')
    logger.debug(added)
    added, names = names.add_many(items, category='item')
    logger.debug(added)
    added, names = names.add_many(rooms, category='room')
    logger.debug(added)
    added, names = names.add_many(paths, category='path')
    logger.debug(added)
    for room in rooms:
        locations = locations.add_node(room, category='room')
    for path in paths:
        locations = locations.add_node(path, category='path')
        world_map = world_map.add_path(names, path)
    locations = load_start_locations(names, locations)

    rules = WorldRules()
    rules = rules.add_actions(actions)

    return rules, World(
        init_locations=locations,
        init_map=world_map,
        init_names=names
    )
