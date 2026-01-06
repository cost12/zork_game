from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="Man Cave",
        description_context=PlainTextContext("You enter a well-furnished man cave. Posters of scanty models, brawny wrestlers, and feline predators adorn every inch of wall."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[name_space.get_from_id("bully", "actor")] TODO
    )

    name_space.add_many([location])
