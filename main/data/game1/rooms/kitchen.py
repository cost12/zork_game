from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="Kitchen",
        description_context=PlainTextContext("You are standing in a modest kitchen. You hear a rush of footsteps in a nearby room."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[name_space.get_from_id("cabinet",      "target"),name_space.get_from_id("stove",        "target"),name_space.get_from_id("kitchen sink", "target")] TODO
    )

    name_space.add_many([location])
