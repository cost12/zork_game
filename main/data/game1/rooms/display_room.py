from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="cushion",
        description_context=ContentsContext("On a velvet cushion rests", "A velvet cushion sits on a pedestal, notably missing the precious item it seems to be meant to hold."),
		description_strategy=ContentsDescription(),
    )

    location = Location(
        name="Display Room",
        description_context=PlainTextContext("You enter a small, dark room with a luxurious velvet carpet."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )

    name_space.add_many([child, location])
