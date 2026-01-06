from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    shelf3 = LocationDetail(
        name="shelf 3",
        description_context=ContentsContext("On the third slot there is", None),
		description_strategy=ContentsDescription(),
    )

    shelf4 = LocationDetail(
        name="shelf 4",
        description_context=ContentsContext("On the fourth slot there is", None),
		description_strategy=ContentsDescription(),
    )

    shelf5 = LocationDetail(
        name="shelf 5",
        description_context=ContentsContext("On the fifth slot there is", None),
		description_strategy=ContentsDescription(),
    )

    shelf6 = LocationDetail(
        name="shelf 6",
        description_context=ContentsContext("On the sixth slot there is", None),
		description_strategy=ContentsDescription(),
    )

    shelf7 = LocationDetail(
        name="shelf 7",
        description_context=ContentsContext("On the seventh slot there is", None),
		description_strategy=ContentsDescription(),
    )

    shelf8 = LocationDetail(
        name="shelf 8",
        description_context=ContentsContext("On the eighth slot there is", None),
		description_strategy=ContentsDescription(),
    )

    shelf9 = LocationDetail(
        name="shelf 9",
        description_context=ContentsContext("On the ninth slot there is", None),
		description_strategy=ContentsDescription(),
    )

    location = Location(
        name="Library",
        description_context=PlainTextContext("You are standing in a small town library. The single room contains ten shelves numbered 1-10."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(
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
        ),
        #children=[shelf3, shelf4, shelf5, shelf6, shelf7, shelf8, shelf9] TODO
    )

    name_space.add_many([shelf3, shelf4, shelf5, shelf6, shelf7, shelf8, shelf9, location])
