from models.actors              import Location, MultiEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, CharacterAchievementContext, CharacterAchievementRestriciton, ItemPlacementContext, ItemPlacementRestriction, ItemStateContext, ItemStateRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = MultiEndPath(
        name="Gym North Exit",
        description=Description[PlainTextContext](PlainTextContext("A metal doorway leads north."), PlainTextDescription()),
        end=StandIn[Location]("pool", "location"),
        multi_end={
            name_space.get_from_id("bongo", "target") : StandIn("Theatre stage", "location")
        },
        passing_requirements=[
            Restriction[CharacterAchievementContext](CharacterAchievementContext(name_space.get_from_id("score", "achievement"), "You can't seem to exit."), CharacterAchievementRestriciton())
        ]
    )

    child = LocationDetail(
        name="rack",
        description=Description[ContentsContext](ContentsContext("Sitting on a simple and sturdy rack is", "A small pyramid-shamed weight rack stands empty before the poster of Arnold."), ContentsDescription()),
        children=[name_space.get_from_id("weights", "target")]
    )

    location = Location(
        name="Gym",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a vintage-feeling gymnasium that feels strangely familiar. On one end is a basketball hoop and a weight rack at the opposite end. Behind the weight rack is a poster of Arnold Schwarzeneger holding up three fingers."), PlainTextDescription()),
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
