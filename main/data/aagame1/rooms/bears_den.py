from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Bear's Den North Exit",
        description=Description[PlainTextContext](PlainTextContext("A narrow escape leads north."), PlainTextDescription()),
        end=StandIn[Location]("Cold Room", "location")
    )

    south_path = SingleEndPath(
        name="Bear's Den South Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads south."), PlainTextDescription()),
        end=StandIn[Location]("Puzzle Room", "location")
    )

    location = Location(
        name="Bear's Den",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a round, earthen den, reeking sickly sweet. A huge, hulking bear blocks a passageway to the North. In an alcove in the Eastern wall is a pile of large, empty jars decorated with what looks like simple depictions of bees."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north',  'direction') : north_path,
            name_space.get_from_id('south',  'direction') : south_path
        },
        children=[name_space.get_from_id("bear", "target")],
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
    name_space.add_many([north_path, south_path, location])
