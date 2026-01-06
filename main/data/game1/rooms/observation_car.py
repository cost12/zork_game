from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="Observation Car",
        description_context=PlainTextContext("You are standing in a train whose walls and ceilings are entirely made of glass. In every direction you can see ocean stretching endlessly. A plucked flurry of a song plays."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )

    name_space.add_many([location])
