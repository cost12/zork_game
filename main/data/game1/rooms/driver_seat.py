from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="mirror",
        description_context=ContentsContext("Hanging from the neck of the rearview mirror is", "The rearview mirror is undecorated, and with it you can see into the empty lot"),
		description_strategy=ContentsDescription(),
    )

    location = Location(
        name="Driver's Seat",
        description_context=PlainTextContext("You sit in the driver's seat of the car, feeling the cool leather on your bottom."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )

    name_space.add_many([child, location])
