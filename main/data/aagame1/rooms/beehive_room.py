from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Beehive Room North Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage goes north."), PlainTextDescription()),
        end=StandIn[Location]("Small Cavern", "location")
    )

    northwest_path = SingleEndPath(
        name="Beehive Room Northwest Exit",
        description=Description[PlainTextContext](PlainTextContext("A rustic door lies to the northwest."), PlainTextDescription()),
        end=StandIn[Location]("barn", "location")
    )

    northeast_path = SingleEndPath(
        name="Beehive Room Northeast Exit",
        description=Description[PlainTextContext](PlainTextContext("A thick metal door leads northeast."), PlainTextDescription()),
        end=StandIn[Location]("armory", "location")
    )

    southeast_path = SingleEndPath(
        name="Beehive Room Southeast Exit",
        description=Description[PlainTextContext](PlainTextContext("A small door goes southeast."), PlainTextDescription()),
        end=StandIn[Location]("Skate Park", "location")
    )

    southwest_path = SingleEndPath(
        name="Beehive Room Southwest Exit",
        description=Description[PlainTextContext](PlainTextContext("A large rocky passage leads southwest."), PlainTextDescription()),
        end=StandIn[Location]("Giant Cave", "location")
    )

    south_path = SingleEndPath(
        name="Beehive Room South Exit",
        description=Description[PlainTextContext](PlainTextContext("A scarred wooden door lies to the south"), PlainTextDescription()),
        end=StandIn[Location]("Orge Lair", "location")
    )

    child = LocationDetail(
        name="toilet",
        description=Description[ContentsContext](ContentsContext("Dripping from a large, intricate beehive is", "A large beehive buzzes with busy energy."), ContentsDescription()),
        children=[StandIn("honey", "target")]
    )

    location = Location(
        name="Beehive Room",
        description=Description[PlainTextContext](PlainTextContext("You enter an odd, hexagonal room and immediately hear a loud buzzing sound. Bees fill the room, their hive in a corner to the east, dripping with honey. Passages are placed on each of the six gray concrete walls."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north',     'direction') : north_path,
            name_space.get_from_id('northwest', 'direction') : northwest_path,
            name_space.get_from_id('northeast', 'direction') : northeast_path,
            name_space.get_from_id('southeast', 'direction') : southeast_path,
            name_space.get_from_id('south',     'direction') : south_path,
            name_space.get_from_id('southwest', 'direction') : southwest_path
        },
        children=[child, name_space.get_from_id("bear", "target")],
        action_restrictions={
            name_space.get_from_id("look", "action") : [
                Restriction[ItemStateContext](
                    ItemStateContext(name_space.get_from_id("lantern", "target"), name_space.get_from_id("on", "state"), "You try to look, but you can't see a thing."), ItemStateRestriction()
                ),
                Restriction[ItemPlacementContext](
                    ItemPlacementContext(name_space.get_from_id("lantern", "target"), name_space.get_from_id("armory", "location"), "You try to look but you can't see a thing."), ItemPlacementRestriction()
                )
            ]
        },
    )
    name_space.add_many([north_path, northeast_path, northwest_path, southeast_path, southwest_path, south_path, child, location])
