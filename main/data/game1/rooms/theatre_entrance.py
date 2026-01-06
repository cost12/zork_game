from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="Theatre Entrance",
        description_context=PlainTextContext("You are standing at the back of a large Theatre. Above grandiose wall decor to the North are the words: \"The Conductor's Job is to Make the Music Enter as a Sheaf of Scores and Leave as a Single Instrument. Music Truly Transports Us.\""),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )

    name_space.add_many([location])
