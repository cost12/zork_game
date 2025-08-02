from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Coach Car North Exit",
        description=Description[PlainTextContext](PlainTextContext("The trian continues to the north."), PlainTextDescription()),
        end=StandIn[Location]("Dining Car", "location")
    )

    south_path = SingleEndPath(
        name="Coach Car South Exit",
        description=Description[PlainTextContext](PlainTextContext("A sliding door leads south."), PlainTextDescription()),
        end=StandIn[Location]("Museum Gallery", "location")
    )

    child = LocationDetail(
        name="seated",
        description=Description[ContentsContext](ContentsContext("Sitting idly on a chair is", "All of the seats lie empty"), ContentsDescription()),
        children=[name_space.get_from_id("child", "actor")]
    )

    location = Location(
        name="Coach Car",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a dark, musty shipping container. Its contents are long gone, and only a few piles of rust remain. You hear a shrill sliding melody playing through some hidden speakers."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[child]
    )
    name_space.add_many([north_path, south_path, child, location])
