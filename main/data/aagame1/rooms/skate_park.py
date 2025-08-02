from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction, CharacterAchievementContext, CharacterAchievementRestriciton

def add_to_name_space(name_space:NameFinder) -> None:
    northwest_path = SingleEndPath(
        name="Skate Park North Exit",
        description=Description[PlainTextContext](PlainTextContext("An exit leads northwest."), PlainTextDescription()),
        end=StandIn[Location]("beehive room", "location")
    )

    south_path = SingleEndPath(
        name="Skate Park South Exit",
        description=Description[PlainTextContext](PlainTextContext(None), PlainTextDescription()),
        end=StandIn[Location]("greenhouse", "location"),
        hidden_when_locked=True,
        passing_requirements=[
            Restriction[CharacterAchievementContext](CharacterAchievementContext(name_space.get_from_id("gift skateboard to child", "achievement"), "A mysterious force prevents you from exiting."), CharacterAchievementRestriciton())
        ]
    )

    location = Location(
        name="Skate Park",
        description=Description[PlainTextContext](PlainTextContext("You stand at the top of a halfpipe at one edge of a small yet complex skate park. Graffiti covers the concrete walls and much of the undulating ground. A poster of Tony Hawk adorns one wall."), PlainTextDescription()),
        paths={
            name_space.get_from_id('northwest', 'direction') : northwest_path,
            name_space.get_from_id('south',     'direction') : south_path
        },
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
    name_space.add_many([south_path, northwest_path, location])
