from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="toilet",
        description_context=ContentsContext("Sitting next to the toilet is", "The toilet seat glints with grime and muck."),
        description_strategy=ContentsDescription(),
    )

    location = Location(
        name="Bathroom",
        description_context=PlainTextContext("You are in a basic bathroom. A toilet, sink, and small shower take up the space, lit by a grimy ceiling light. There is no water in the toilet bowl."),
        description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )

    name_space.add_many([child, location])
