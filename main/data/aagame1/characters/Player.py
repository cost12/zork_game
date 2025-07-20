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
        id="player1 inventory",
        item_limit=ItemLimit(40, 100)
    )

    player = Actor(
        name="player1",
        type="player",
        description=(plain_text, "well, it's you"),
        states=sdg,
        skills=name_space.get_from_id("standard"),
        children=[inventory],
        target_responses={
            name_space.get_from_id("look",   "action") : StaticResponse("You look at your hands, grappling with the deeds they have done."),
            name_space.get_from_id("take",   "action") : StaticResponse("Trust us, you are already quite taken with yourself."),
            name_space.get_from_id("attack", "action") : StaticResponse("With what? Trust us, it gets better.")
        }
    )

    name_space.add_many([player,inventory])
