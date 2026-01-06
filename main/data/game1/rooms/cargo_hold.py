from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="Cargo Hold",
        description_context=PlainTextContext("You are standing in a dark, musty shipping container. Its contents are long gone, and only a few piles of rust remain. You hear a shrill sliding melody playing through some hidden speakers."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )
    name_space.add_many([location])
