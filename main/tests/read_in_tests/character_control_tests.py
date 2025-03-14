from tests.conftest             import controls
from factories.factories        import CharacterControlFactory
from models.character           import Character
from controls.character_control import CharacterController

def test_read_in(controls:CharacterControlFactory):
    for character, controller in controls.characters.items():
        assert isinstance(character, Character)
        assert isinstance(controller, CharacterController)
    assert controls.playable_characters() > 0