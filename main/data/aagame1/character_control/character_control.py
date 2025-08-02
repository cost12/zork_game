from controls.character_control import NPCController, CommandLineController
from factories.factories        import CharacterControlFactory
from utils.relator              import NameFinder

def get_character_control(name_space:NameFinder) -> CharacterControlFactory:
    controls = CharacterControlFactory()
    controls.create_character(name_space.get_from_id("bully",   "actor"), NPCController())
    controls.create_character(name_space.get_from_id("orge",    "actor"), NPCController())
    controls.create_character(name_space.get_from_id("bear",    "actor"), NPCController())
    controls.create_character(name_space.get_from_id("child",   "actor"), NPCController())
    controls.create_character(name_space.get_from_id("player1", "actor"), CommandLineController())
    return controls
