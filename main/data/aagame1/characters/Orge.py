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
        id="orge inventory",
        item_limit=ItemLimit(200, 100)
    )

    orge = Actor(
        name="Orge",
        type="orge",
        description=(plain_text, "an Orge (very different from an Ogre), a hulking brute, more scar tissue than clear skin, greenish, rank, and steaming."),
        states=sdg,
        skills=name_space.get_from_id("standard"),
        children=[inventory],
        target_responses={
            name_space.get_from_id("look",   "action") : StaticResponse("You feel repulsed as you look at the Orge and struggle to keep it within its gaze."),
            name_space.get_from_id("take",   "action") : StaticResponse("A foolish endeavor."),
            name_space.get_from_id("attack", "action") : StaticResponse("You attack the orge, damaging it's swolen ego"),
            name_space.get_from_id("hug",    "action") : StaticResponse("This merely confuses and angers the Orge."),
            name_space.get_from_id("kiss",   "action") : StaticResponse("The Orge thinks you are cute and kisses you back. With gusto!")
        }
    )

    name_space.add_many([orge,inventory])
