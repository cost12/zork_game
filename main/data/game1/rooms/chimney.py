from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="Chimney",
        description_context=PlainTextContext("You are standing in a cramped dark space. It smells of smoke. You are quickly covered in soot and ash. Blegh!"),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo()
    )

    name_space.add_many([location])
