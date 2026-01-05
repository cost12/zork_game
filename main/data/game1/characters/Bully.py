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

    inventory = get_inventory(StandIn('bully', 'actor'), ItemLimit(200, 100))
    wearing   = get_wearing(  StandIn('bully', 'actor'), ItemLimit(10, 10))

    bully = Actor(
        name="Bully",
        description_context=PlainTextContext("a larger fellow with a pink face. He looks strong of body, but perhaps not of mind."),
        description_strategy=PlainTextDescription(),
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("look",   "action") : plain_text_description("You feel somewhat offput looking at the bully, for he leers at you languidly, breathing through his mouth."),
                name_space.get_from_id("take",   "action") : plain_text_description("You couldn't if you tried."),
                name_space.get_from_id("attack", "action") : plain_text_description("With what?"),
                name_space.get_from_id("hug",    "action") : plain_text_description("The bully calls you the f-slur!"),
                name_space.get_from_id("kiss",   "action") : plain_text_description("The bully calls you the f-slur!"),
                name_space.get_from_id("compliment", "action") : plain_text_description("The bully dismisses you, but he blushes a little...")
            }
        ),
        actor_info=ActorInfo(
            skills=name_space.get_from_id("standard"),
            inventory=inventory,
            wearing=wearing,
        )
    )

    name_space.add_many([bully,inventory,wearing])
