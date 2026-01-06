from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="table",
        name_id="table2",
        description_context=ContentsContext("On the table sits", "The table is bare and free of burden. That must be nice"),
		description_strategy=ContentsDescription(),
        #children=[name_space.get_from_id("plate", "target")] TODO
    )

    location = Location(
        name="Dining Room",
        description_context=PlainTextContext("You are standing in a rectangular room with a rough-hewn wooden table in the middle."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[child] TODO
    )

    name_space.add_many([child, location])
