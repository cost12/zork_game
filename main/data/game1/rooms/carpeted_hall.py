from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="Carpeted Hall",
        description_context=PlainTextContext("You stand in a long torch-lit hallway adorned with an ornate, illustrative carpet stretching as far as you can see to the East."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo()
    )

    name_space.add_many([location])
