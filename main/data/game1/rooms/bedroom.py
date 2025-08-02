from models.actors              import Actor, Target, Location, LocationDetail, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import DescriptionStrategy, DescriptionContext, Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext

class FstringDescription(DescriptionStrategy[Target]):
    def describe(self, context:DescriptionContext, specific:Target) -> str:
        return f"Above your head is {specific.get_description_to(context.character)} in the ceiling."

def add_to_name_space(name_space:NameFinder) -> None:
    east_path = SingleEndPath(
        name="Bedroom East Exit",
        description="To the east, you see a doorway.",
        end=StandIn[Location]("Bathroom", "location")
    )

    up_path = SingleEndPath(
        name="Bedroom Up Exit",
        description=Description[Target](StandIn[Target]("trapdoor", "target"), FstringDescription()),
        end=StandIn[Location]("Attic", "location"),
        children=[StandIn[Target]("trapdoor", "target")],
        passing_requirements={
            Restriction[ItemStateContext](ItemStateContext(name_space.get_from_id("trapdoor", "target"), name_space.get_from_id("opened", "state"), "The trapdoor is closed."), ItemStateRestriction())
        }
    )

    south_path = SingleEndPath(
        name="Bedroom South Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage stretches south."), PlainTextDescription()),
        end=StandIn[Location]("Hallway", "location")
    )

    bedside = LocationDetail(
        name="Bedside",
        description=Description[ContentsContext](ContentsContext("On the bedside table rests", "Next to the bed sits an empty table."), ContentsDescription()),
        children=[StandIn("mug", "target"), StandIn("brown book", "target")]
    )

    bedroom = Location(
        name="Bedroom",
        description=Description[PlainTextContext](PlainTextContext("You are in a humble bedroom. A small bed lines one wall. It looks cozy. Feeble light seeps through a small overhead light."), PlainTextDescription()),
        paths={
            name_space.get_from_id('east',  'direction') : east_path,
            name_space.get_from_id('up',    'direction') : up_path,
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[bedside, StandIn[Actor]("player1", "actor")],
        start_location=True
    )
    name_space.add_many([east_path, up_path, south_path, bedside, bedroom])
