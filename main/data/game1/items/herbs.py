from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",       "state")],
        state_graphs      =[name_space.get_from_id("takeable sg", "stategraph"),
                            name_space.get_from_id("flammable sg", "stategraph"),
                            name_space.get_from_id("fragile_untie sg", "stategraph")],
        name_space        =name_space
    )

    herbs = Target(
        name="dried herbs",
        aliases=["herbs"],
        description_context=PlainTextContext("a small, tightly packed bundle of herbs bound by a short length of hemp twine"),
        description_strategy=PlainTextDescription(),
        weight=1,
        value=1,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("burn",  "action") : plain_text_description("With what?"),
                name_space.get_from_id("untie", "action") : plain_text_description("You untie the bundle. The hempen twine disintigrates at your touch, and the herbacious leaves fall to the ground, scattered. You cannot gather them.")
            },
            state_responses={
                name_space.get_from_id("broken", "state") : plain_text_description("You scatter the desicated leaves to the ground")
            }
        )
    )

    name_space.add(herbs)
