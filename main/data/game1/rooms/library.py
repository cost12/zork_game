from models.actors              import Location, MultiEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = MultiEndPath(
        name="Library North Exit",
        description=Description[PlainTextContext](PlainTextContext("A regal yet sturdy double door leads north."), PlainTextDescription()),
        end=StandIn[Location]("puzzle room", "location"),
        multi_end={
            name_space.get_from_id("violin", "target") : StandIn("theatre stage", "location")
        },
        passing_requirements=[
            Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("red book", "target"), StandIn("shelf 3 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
            Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("gray book", "target"), StandIn("shelf 4 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
            Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("brown book", "target"), StandIn("shelf 5 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
            Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("yellow book", "target"), StandIn("shelf 6 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
            Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("emerald book", "target"), StandIn("shelf 7 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
            Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("burgundy book", "target"), StandIn("shelf 8 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
            Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("vermilion book", "target"), StandIn("shelf 9 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction())
        ]
    )

    shelf3 = LocationDetail(
        name="shelf 3",
        description=Description[ContentsContext](ContentsContext("On the third slot there is", None), ContentsDescription())
    )

    shelf4 = LocationDetail(
        name="shelf 4",
        description=Description[ContentsContext](ContentsContext("On the fourth slot there is", None), ContentsDescription())
    )

    shelf5 = LocationDetail(
        name="shelf 5",
        description=Description[ContentsContext](ContentsContext("On the fifth slot there is", None), ContentsDescription())
    )

    shelf6 = LocationDetail(
        name="shelf 6",
        description=Description[ContentsContext](ContentsContext("On the sixth slot there is", None), ContentsDescription())
    )

    shelf7 = LocationDetail(
        name="shelf 7",
        description=Description[ContentsContext](ContentsContext("On the seventh slot there is", None), ContentsDescription())
    )

    shelf8 = LocationDetail(
        name="shelf 8",
        description=Description[ContentsContext](ContentsContext("On the eighth slot there is", None), ContentsDescription())
    )

    shelf9 = LocationDetail(
        name="shelf 9",
        description=Description[ContentsContext](ContentsContext("On the ninth slot there is", None), ContentsDescription())
    )

    location = Location(
        name="Library",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a small town library. The single room contains ten shelves numbered 1-10."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path
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
        },
        children=[shelf3, shelf4, shelf5, shelf6, shelf7, shelf8, shelf9]
    )
    name_space.add_many([shelf3, shelf4, shelf5, shelf6, shelf7, shelf8, shelf9, north_path, location])
