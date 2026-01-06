from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="counter",
        description_context=ContentsContext("On the counter is", "The counter is empty. Sound familiar?"),
		description_strategy=ContentsDescription(),
    )

    location = Location(
        name="Dining Car",
        description_context=PlainTextContext("You are in the conductor's car. A complex control panel is next to an exit at the North of the car. An elegant violin concerto plays through the room's speakers."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )

    name_space.add_many([child, location])
