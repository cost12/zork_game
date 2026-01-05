from utils.relator              import NameFinder
from models.actors              import Actor, ItemLimit, TargetInfo, ActorInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils               import sdg_from_parts, get_inventory, get_wearing
from readin.stand_in            import StandIn

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        name_space=name_space,
        state_graphs=[name_space.get_from_id("standard_character")]
    )

    inventory = get_inventory(StandIn('orge', 'actor'), item_limit=ItemLimit(200, 100))
    wearing   = get_wearing  (StandIn('orge', 'actor'), item_limit=ItemLimit(10, 10))

    orge = Actor(
        name="Orge",
        description_context=PlainTextContext("an Orge (very different from an Ogre), a hulking brute, more scar tissue than clear skin, greenish, rank, and steaming."),
        description_strategy=PlainTextDescription(),
        actor_info=ActorInfo(
            skills=name_space.get_from_id("standard"),
            inventory=inventory,
            wearing=wearing,
        ),
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("look",   "action") : plain_text_description("You feel repulsed as you look at the Orge and struggle to keep it within its gaze."),
                name_space.get_from_id("take",   "action") : plain_text_description("A foolish endeavor."),
                name_space.get_from_id("attack", "action") : plain_text_description("You attack the orge, damaging it's swolen ego"),
                name_space.get_from_id("hug",    "action") : plain_text_description("This merely confuses and angers the Orge."),
                name_space.get_from_id("kiss",   "action") : plain_text_description("The Orge thinks you are cute and kisses you back. With gusto!")
            }
        )
    )

    name_space.add_many([orge,inventory,wearing])
