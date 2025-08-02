from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    south_path = SingleEndPath(
        name="Office South Exit",
        description=Description[PlainTextContext](PlainTextContext("A doorway leads southward."), PlainTextDescription()),
        end=StandIn[Location]("dining room", "location"),
    )

    child = LocationDetail(
        name="desk",
        description=Description[ContentsContext](ContentsContext("Sitting on the desk is", "The desk is lacking any contents."), ContentsDescription()),
        children=[
            name_space.get_from_id("emerald book", "target"), 
            name_space.get_from_id("magnifying glass", "target")
        ]
    )

    location = Location(
        name="Office",
        description=Description[PlainTextContext](PlainTextContext("You are in a simple home office. At a desk sits a large, heavy desktop computer open to a console, its light eerily illuminating the room with a blue glow. There is a spindly chair at the desk."), PlainTextDescription()),
        paths={
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[child]
    )
    name_space.add_many([child, south_path, location])
