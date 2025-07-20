from utils.relator              import NameFinder
from models.actors              import Actor, LocationDetail, ItemLimit
from models.response            import StaticResponse
from readin.description_helpers import plain_text
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        name_space=name_space,
        state_graphs=[name_space.get_from_id("standard_character")]
    )

    inventory = LocationDetail(
        name="inventory",
        id="child inventory",
        item_limit=ItemLimit(20, 100)
    )

    bear = Actor(
        name="Child",
        type="standard",
        description=(plain_text, "a small child with a face reflecting acquired ugliness"),
        states=sdg,
        skills=name_space.get_from_id("standard"),
        children=[inventory],
        target_responses={
            name_space.get_from_id("look",   "action") : StaticResponse("You feel sorry for the lonesome child. They do not meet your gaze."),
            name_space.get_from_id("take",   "action") : StaticResponse("Amber alert!"),
            name_space.get_from_id("attack", "action") : StaticResponse("A child???"),
            name_space.get_from_id("hug",    "action") : StaticResponse("This briefly comforts the sorry child."),
            name_space.get_from_id("kiss",   "action") : StaticResponse("Okay Drake")
        }
    )

    name_space.add_many([bear,inventory])
