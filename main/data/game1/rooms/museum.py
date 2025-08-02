from models.actors              import Location, MultiEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemPlacementContext, ItemPlacementRestriction, ItemStateContext, ItemStateRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = MultiEndPath(
        name="Gym North Exit",
        description=Description[PlainTextContext](PlainTextContext("A curtained passage proceeds northwards."), PlainTextDescription()),
        end=StandIn[Location]("coach car", "location"),
        multi_end={
            name_space.get_from_id("lyre", "target") : StandIn("Theatre stage", "location")
        }
    )

    child = LocationDetail(
        name="wall",
        description=Description[ContentsContext](ContentsContext("Hanging alone on the desolate walls is ", None), ContentsDescription()),
        children=[name_space.get_from_id("hercules", "target")]
    )

    location = Location(
        name="Museum Gallery",
        description=Description[PlainTextContext](PlainTextContext("You are standing at the edge of a glorious museum gallery. The walls are gilded and enshrined with curlicue Rococo Era filigree. The walls are sadly bare."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path
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
    name_space.add_many([child, north_path, location])
