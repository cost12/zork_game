from models.actors              import Location, LocationDetail, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    east_path = SingleEndPath(
        name="Barn East Exit",
        description=Description[PlainTextContext](PlainTextContext("A large barn door leads east"), PlainTextDescription()),
        end=StandIn[Location]("Beehive Room", "location")
    )

    child = LocationDetail(
        name="spear rack",
        description=Description[ContentsContext](ContentsContext("On a spear rack there is", "An empty spear rack is on one wall."), ContentsDescription()),
        item_responses={
            name_space.get_from_id("spear", "target") : "A poof of smoke appears."
        },
        children=[StandIn("rubber ducky", "target")]
    )

    child2 = LocationDetail(
        name="pitchfork rack",
        description=Description[ContentsContext](ContentsContext("On a rack for pitchforks is", "An empty pitchfork rack rests on one wall."), ContentsDescription()),
        item_responses={
            name_space.get_from_id("pitchfork", "target") : "A poof of smoke appears."
        },
        children=[StandIn("warm boots", "target")]
    )

    location = Location(
        name="Barn",
        description=Description[PlainTextContext](PlainTextContext("You are in a large empty barn dominated by what seem to be abandoned stables. Cobwebs cover most surfaces. On the west wall, opposite the door, ancient tools are rusted to their racks, with a single holder missing something like a rake or staff."), PlainTextDescription()),
        paths={
            name_space.get_from_id('east',  'direction') : east_path
        },
        children=[child, child2]
    )
    name_space.add_many([east_path, child, child2, location])
