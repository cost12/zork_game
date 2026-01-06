from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="wall",
        description_context=ContentsContext("Hanging from a peg in the wall is", None),
		description_strategy=ContentsDescription(),
    )

    location = Location(
        name="Greenhouse",
        description_context=PlainTextContext("You stand in the middle of a large, deserted greenhouse. Any plants that grew here are long dead."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )

    name_space.add_many([child, location])
