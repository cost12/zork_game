from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    out_path = SingleEndPath(
        name="Driver's Seat Out Exit",
        description=Description[PlainTextContext](PlainTextContext("The door leads out."), PlainTextDescription()),
        end=StandIn[Location]("parking lot", "location")
    )

    child = LocationDetail(
        name="mirror",
        description=Description[ContentsContext](ContentsContext("Hanging from the neck of the rearview mirror is", "The rearview mirror is undecorated, and with it you can see into the empty lot"), ContentsDescription()),
        children=[name_space.get_from_id("sunglasses", "target")]
    )

    location = Location(
        name="Driver's Seat",
        description=Description[PlainTextContext](PlainTextContext("You sit in the driver's seat of the car, feeling the cool leather on your bottom."), PlainTextDescription()),
        paths={
            name_space.get_from_id('out',  'direction') : out_path
        },
        children=[child],
    )

    name_space.add_many([child, location, out_path])
