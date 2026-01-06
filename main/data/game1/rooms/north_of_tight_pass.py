from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="North of Tight Pass",
        description_context=PlainTextContext("You stand in a small, narrow cave."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[name_space.get_from_id("bully", "actor")] TODO
    )

    name_space.add_many([location])
