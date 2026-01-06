from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="Cellar",
        description_context=PlainTextContext("You enter a damp, dark cellar with stone walls. Water leaks down one wall slowly. In a corner is a large trunk."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[name_space.get_from_id("trunk", "target")] TODO
    )

    name_space.add_many([location])
