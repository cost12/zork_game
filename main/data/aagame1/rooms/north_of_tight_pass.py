from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="North of Tight Pass North Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads to the north, emitting an unpleasant odor."), PlainTextDescription()),
        end=StandIn[Location]("man cave", "location")
    )

    south_path = SingleEndPath(
        name="North of Tight Pass South Exit",
        description=Description[PlainTextContext](PlainTextContext("The tight pass continues south."), PlainTextDescription()),
        end=StandIn[Location]("south of tight pass", "location")
    )

    location = Location(
        name="North of Tight Pass",
        description=Description[PlainTextContext](PlainTextContext("You stand in a small, narrow cave."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[name_space.get_from_id("bully", "actor")]
    )
    name_space.add_many([south_path, north_path, location])
