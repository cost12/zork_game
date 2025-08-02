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
        id="bully inventory",
        item_limit=ItemLimit(200, 100)
    )

    bully = Actor(
        name="Bully",
        type="standard",
        description=(plain_text, "a larger fellow with a pink face. He looks strong of body, but perhaps not of mind."),
        states=sdg,
        skills=name_space.get_from_id("standard"),
        children=[inventory],
        target_responses={
            name_space.get_from_id("look",   "action") : StaticResponse("You feel somewhat offput looking at the bully, for he leers at you languidly, breathing through his mouth."),
            name_space.get_from_id("take",   "action") : StaticResponse("You couldn't if you tried."),
            name_space.get_from_id("attack", "action") : StaticResponse("With what?"),
            name_space.get_from_id("hug",    "action") : StaticResponse("The bully calls you the f-slur!"),
            name_space.get_from_id("kiss",   "action") : StaticResponse("The bully calls you the f-slur!"),
            name_space.get_from_id("compliment", "action") : StaticResponse("The bully dismisses you, but he blushes a little...")
        }
    )

    name_space.add_many([bully,inventory])
