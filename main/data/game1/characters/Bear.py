from utils.relator              import NameFinder
from models.actors              import Actor, ItemLimit, TargetInfo, ActorInfo
from readin.description_helpers import PlainTextContext, PlainTextDescription, plain_text_description
from readin.utils               import sdg_from_parts, get_inventory, get_wearing
from readin.stand_in            import StandIn

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        name_space=name_space,
        state_graphs=[name_space.get_from_id("standard_character")]
    )

    inventory = get_inventory(StandIn('bear', 'actor'), ItemLimit(200, 100))
    wearing   = get_wearing(  StandIn('bear', 'actor'), ItemLimit(15, 15))

    bear = Actor(
        name="Bear",
        description_context=PlainTextContext("a bear."),
        description_strategy=PlainTextDescription(),
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("look",   "action") : plain_text_description("You see a bear"),
                name_space.get_from_id("take",   "action") : plain_text_description("A foolish endeavor."),
                name_space.get_from_id("attack", "action") : plain_text_description("With what?"),
                name_space.get_from_id("hug",    "action") : plain_text_description("This merely confuses and angers the Bear"),
                name_space.get_from_id("kiss",   "action") : plain_text_description("The Bear thinks you are cute and kisses you back. With gusto!")
            }
        ),
        actor_info=ActorInfo(
            inventory=inventory,
            wearing=wearing,
            skills=name_space.get_from_id('standard'),
        ),
    )

    name_space.add_many([bear,inventory,wearing])
