from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Puzzle Room North Exit",
        description=Description[PlainTextContext](PlainTextContext("A stony passage leads north."), PlainTextDescription()),
        end=StandIn[Location]("bear's den", "location"),
    )

    south_path = SingleEndPath(
        name="Puzzle Room South Exit",
        description=Description[PlainTextContext](PlainTextContext("A nice walkway leads south"), PlainTextDescription()),
        end=StandIn[Location]("library", "location")
    )

    child = LocationDetail(
        name="table",
        id="puzzle room table",
        description=Description[ContentsContext](ContentsContext("On a spindly table you find", "There is a spindly table in the middle of the room, holding nothing"), ContentsDescription()),
        children=[name_space.get_from_id("puzzle", "target")]
    )

    location = Location(
        name="Puzzle Room",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a homey room. On a carpet stands a table."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[child],
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
    name_space.add_many([child, south_path, north_path, location])
