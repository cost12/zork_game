from models.actors              import Location, LocationDetail, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    west_path = SingleEndPath(
        name="Bathroom West Exit",
        description=Description[PlainTextContext](PlainTextContext("A thin door leads west, offering no privacy"), PlainTextDescription()),
        end=StandIn[Location]("Beehive Room", "location")
    )

    child = LocationDetail(
        name="toilet",
        description=Description[ContentsContext](ContentsContext("Sitting next to the toilet is", "The toilet seat glints with grime and muck."), ContentsDescription()),
        children=[StandIn("vermilion book", "target")]
    )

    location = Location(
        name="Bathroom",
        description=Description[PlainTextContext](PlainTextContext("You are in a basic bathroom. A toilet, sink, and small shower take up the space, lit by a grimy ceiling light. There is no water in the toilet bowl."), PlainTextDescription()),
        paths={
            name_space.get_from_id('west',  'direction') : west_path
        },
        children=[child, name_space.get_from_id("shower", "target"), name_space.get_from_id("sink", "target")]
    )
    name_space.add_many([west_path, child, location])
