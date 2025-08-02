from models.actors              import Location, LocationDetail, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    west_path = SingleEndPath(
        name="Armory West Exit",
        description="A harsh looking metal doorway leads west.",
        end=StandIn[Location]("Beehive Room", "location")
    )

    rack = LocationDetail(
        name="rack",
        description=Description[ContentsContext](ContentsContext("Hanging on a well-worn wooden rack is", "An empty weapons rack hangs on the wall."), ContentsDescription()),
        children=[StandIn("spear", "target"), StandIn("pitchfork", "target"), StandIn("sword", "target")]
    )

    armory = Location(
        name="Armory",
        description=Description[PlainTextContext](PlainTextContext("You stand in an old armory that once held many armaments and much armor. All that remains are a few neglected weapons. On the floor is a mosaic resembling an hourglass with both glass canisters cracked."), PlainTextDescription()),
        paths={
            name_space.get_from_id('west',  'direction') : west_path
        },
        action_restrictions={
            name_space.get_from_id("take", "action") : Restriction[ItemStateContext](
                ItemStateContext(name_space.get_from_id("hourglass", "target"), name_space.get_from_id("broken", "state"), "As you move to place the item in your inventory, it turns to dust. As if guided by some ancient curse it slips through your fingers and reforms in it's previous location."), ItemStateRestriction()
            ),
            name_space.get_from_id("look", "action") : [
                Restriction[ItemStateContext](
                    ItemStateContext(name_space.get_from_id("lantern", "target"), name_space.get_from_id("on", "state"), "You try to look, but you can't see a thing."), ItemStateRestriction()
                ),
                Restriction[ItemPlacementContext](
                    ItemPlacementContext(name_space.get_from_id("lantern", "target"), name_space.get_from_id("armory", "location"), "You try to look but you can't see a thing."), ItemPlacementRestriction()
                )
            ]
        },
        children=[rack]
    )
    name_space.add_many([west_path, rack, armory])
