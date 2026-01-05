from utils.relator              import NameFinder
from models.actors              import Actor, ItemLimit, ActorInfo, TargetInfo
from readin.description_helpers import PlainTextContext, PlainTextDescription, plain_text_description
from readin.utils               import sdg_from_parts, get_inventory, get_wearing
from readin.stand_in            import StandIn

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        name_space=name_space,
        state_graphs=[name_space.get_from_id("standard_character")]
    )

    inventory = get_inventory(StandIn('player1', 'actor'), item_limit=ItemLimit(40, 100))
    wearing   = get_wearing  (StandIn('player1', 'actor'), item_limit=ItemLimit(10,10))

    player = Actor(
        name="player1",
        description_context=PlainTextContext("well, it's you"),
        description_strategy=PlainTextDescription(),
        actor_info=ActorInfo(
            skills=name_space.get_from_id("standard"),
            inventory=inventory,
            wearing=wearing,
        ),
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("look",   "action") : plain_text_description("You look at your hands, grappling with the deeds they have done."),
                name_space.get_from_id("take",   "action") : plain_text_description("Trust us, you are already quite taken with yourself."),
                name_space.get_from_id("attack", "action") : plain_text_description("With what? Trust us, it gets better.")
            }
        )
    )

    name_space.add_many([player,inventory,wearing])
