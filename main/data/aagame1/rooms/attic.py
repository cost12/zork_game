from dataclasses                import dataclass

from models.state               import State
from models.actors              import Location, LocationDetail, SingleEndPath, Target
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, DescriptionStrategy, DescriptionContext, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext

@dataclass
class DownContext:
    trapdoor : Target
    opened   : State

class DownDescription(DescriptionStrategy[DownContext]):
    def describe(self, context:DescriptionContext, specific:DownContext) -> str:
        if specific.opened in specific.trapdoor.get_current_state():
            return "At your feet the trapdoor is still open."
        else:
            return "At your feet lies a trapdoor flush with the floor."

def add_to_name_space(name_space:NameFinder) -> None:
    down_path = SingleEndPath(
        name="Attic Down Exit",
        description=Description[DownContext](DownContext(name_space.get_from_id("trapdoor", "target"), name_space.get_from_id("opened", "state")), DownDescription()),
        end=StandIn[Location]("Bedroom", "location"),
        children=[name_space.get_from_id("trapdoor", "target")],
        passing_requirements={
            Restriction[ItemStateContext](ItemStateContext(name_space.get_from_id("trapdoor", "target"), name_space.get_from_id("opened", "state"), "The trapdoor is closed."), ItemStateRestriction())
        }
    )

    child = LocationDetail(
        name="table",
        description=Description[ContentsContext](ContentsContext("On a spindly table you find", "There is a spindly table in the middle of the room."), ContentsDescription()),
        children=[StandIn("leaflet", "target"), StandIn("hourglass", "target"), StandIn("yellow book", "target"), StandIn("lantern", "target")]
    )

    location = Location(
        name="Attic",
        description=Description[PlainTextContext](PlainTextContext("You are in a musty, small attic. It is mostly empty, except for a table. At one end of the room is a sooty brick fireplace, leading upwards to the chimney"), PlainTextDescription()),
        paths={
            name_space.get_from_id('down',  'direction') : down_path
        },
        children=[child]
    )
    name_space.add_many([down_path, child, location])
