from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="spear rack",
        description_context=ContentsContext("On a spear rack there is", "An empty spear rack is on one wall."),
        description_strategy=ContentsDescription(),
        item_responses={
            name_space.get_from_id("spear", "target") : "A poof of smoke appears."
        },
    )

    child2 = LocationDetail(
        name="pitchfork rack",
        description_context=ContentsContext("On a rack for pitchforks is", "An empty pitchfork rack rests on one wall."),
        description_strategy=ContentsDescription(),
        item_responses={
            name_space.get_from_id("pitchfork", "target") : "A poof of smoke appears."
        },
    )

    location = Location(
        name="Barn",
        description_context=PlainTextContext("You are in a large empty barn dominated by what seem to be abandoned stables. Cobwebs cover most surfaces. On the west wall, opposite the door, ancient tools are rusted to their racks, with a single holder missing something like a rake or staff."),
        description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )
    name_space.add_many([child, child2, location])
