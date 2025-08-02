from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Orge Lair North Exit",
        description=Description[PlainTextContext](PlainTextContext("A door leads north."), PlainTextDescription()),
        end=StandIn[Location]("beehive room", "location")
    )

    south_path = SingleEndPath(
        name="Orge Lair South Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads south, glowing slightly."), PlainTextDescription()),
        end=StandIn[Location]("bright room", "location"),
        passing_requirements={
            Restriction[ItemStateContext](ItemStateContext(name_space.get_from_id("orge", "actor"), name_space.get_from_id("guarding", "state"), "In the middle stands a hulking orge holding a large club, blocking the way to a passage going South."), ItemStateRestriction())
        }
    )

    location = Location(
        name="Orge Lair",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a smelly, humid room that smells like a well-used locker room, rancid and almost spicy. Roots poke through the ceiling and crude pornographic etchings cover the walls."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[name_space.get_from_id("orge", "actor")],
        action_restrictions={
            name_space.get_from_id("look", "action") : [
                Restriction[ItemStateContext](
                    ItemStateContext(name_space.get_from_id("lantern", "target"), name_space.get_from_id("on", "state"), "You try to look, but you can't see a thing."), ItemStateRestriction()
                ),
                Restriction[ItemPlacementContext](
                    ItemPlacementContext(name_space.get_from_id("lantern", "target"), name_space.get_from_id("armory", "location"), "You try to look but you can't see a thing."), ItemPlacementRestriction()
                )
            ]
        }
    )
    name_space.add_many([south_path, north_path, location])
