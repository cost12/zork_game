from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="South of Tight Pass North Exit",
        description=Description[PlainTextContext](PlainTextContext("The tight pass leads north."), PlainTextDescription()),
        end=StandIn[Location]("north of tight pass", "location")
    )

    south_path = SingleEndPath(
        name="South of Tight Pass South Exit",
        description=Description[PlainTextContext](PlainTextContext("A frigid draft is coming from a passage leading south."), PlainTextDescription()),
        end=StandIn[Location]("cold room", "location")
    )

    location = Location(
        name="South of Tight Pass",
        description=Description[PlainTextContext](PlainTextContext("You stand in a narrow, claustrophobic cave."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        }
    )
    name_space.add_many([south_path, north_path, location])
