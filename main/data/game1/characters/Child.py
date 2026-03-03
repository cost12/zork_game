from utils.relator              import NameFinder
from models.actors              import Actor, ItemLimit, TargetInfo, ActorInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils               import sdg_from_parts, get_inventory, get_wearing

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        name_space=name_space,
        state_graphs=[name_space.get_from_id("standard_character sg")]
    )

    wearing   = get_wearing('child', item_limit=ItemLimit(10, 10))

    child = Actor(
        name="Child",
        description_context=PlainTextContext("a small child with a face reflecting acquired ugliness"),
        description_strategy=PlainTextDescription(),
        actor_info=ActorInfo(
            inventory=None,
            wearing=wearing,
            skills=name_space.get_from_id("standard"),
        ),
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("look",   "action") : plain_text_description("You feel sorry for the lonesome child. They do not meet your gaze."),
                name_space.get_from_id("take",   "action") : plain_text_description("Amber alert!"),
                name_space.get_from_id("attack", "action") : plain_text_description("A child???"),
                name_space.get_from_id("hug",    "action") : plain_text_description("This briefly comforts the sorry child."),
                name_space.get_from_id("kiss",   "action") : plain_text_description("Okay Drake")
            }
        )
    )

    inventory = get_inventory(child, item_limit=ItemLimit(20, 100))
    child._set_inventory(inventory)

    name_space.add_many([child,inventory,wearing])
