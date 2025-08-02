from models.actors              import Location, SingleEndPath, MultiEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = MultiEndPath(
        name="Theatre Entrance North Exit",
        description=Description[PlainTextContext](PlainTextContext("A gilded double door leads north, slight light streaking through the thin gap running down their seam."), PlainTextDescription()),
        end=None,
        multi_end={
            name_space.get_from_id("baton",         "target") : StandIn("bright room",    "location"),
            name_space.get_from_id("lyre",          "target") : StandIn("museum gallery", "location"),
            name_space.get_from_id("triangle",      "target") : StandIn("parking lot",    "location"),
            name_space.get_from_id("slide whistle", "target") : StandIn("chimney",        "location"),
            name_space.get_from_id("bongo",         "target") : StandIn("gym",            "location"),
            name_space.get_from_id("violin",        "target") : StandIn("library",        "location")
        }
    )

    south_path = SingleEndPath(
        name="Theatre Entrance South Exit",
        description=Description[PlainTextContext](PlainTextContext("The Theatre's seating area lies in the south."), PlainTextDescription()),
        end=StandIn[Location]("theatre seats", "location")
    )

    location = Location(
        name="Theatre Entrance",
        description=Description[PlainTextContext](PlainTextContext("You are standing at the back of a large Theatre. Above grandiose wall decor to the North are the words: \"The Conductor's Job is to Make the Music Enter as a Sheaf of Scores and Leave as a Single Instrument. Music Truly Transports Us.\""), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        }
    )
    name_space.add_many([south_path, north_path, location])
