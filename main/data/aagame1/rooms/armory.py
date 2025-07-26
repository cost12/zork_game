from models.actors import Actor, Target, Location, LocationDetail, SingleEndPath
from models.requirement import ItemStateRequirement
from utils.relator import NameFinder
from readin.stand_in import StandIn
from readin.description_helpers import DescriptionStrategy, DescriptionContext, Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

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
        passing_requirements=ItemStateRequirement({
            StandIn[Target]("trapdoor", "target") : {
                name_space.get_from_id("open", "state") : [True, None]
            }
        })
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

{
    "name"       : "Armory",
    "description": "You stand in an old armory that once held many armaments and much armor. All that remains are a few neglected weapons. On the floor is a mosaic resembling an hourglass with both glass canisters cracked.",
    "paths"      : {
        "west"   : {
            "name"        : "Exit 1",
            "description" : "A harsh looking metal doorway leads west",
            "end"         : "Beehive Room"
        }
    },
    "action_restrictions" : {
        "take" : {
            "item_state_requirements" : {
                "hourglass" : {
                    "broken" : [true, "As you move to place the item in your inventory, it turns to dust. As if guided by some ancient curse it slips through your fingers and reforms in it's previous location."]
                }
            }
        },
        "look" : {
            "item_state_requirements" : {
                "lantern" : {
                    "on" : [true, "You try to look, but you can't see a thing."]
                }
            },
            "item_placement_requirements" : {
                "lantern" : [["Armory", true, "You try to look but you can't see a thing."]]
            }
        }
    },
    "details" : [
        {
            "name"        : "rack",
            "description" : {
                "type"    : "contents",
                "full"    : "Hanging on a well-worn wooden rack is",
                "empty"   : "An empty weapons rack hangs on the wall"
            },
            "contents"    : ["spear", "pitchfork", "sword"]
        }
    ]
}