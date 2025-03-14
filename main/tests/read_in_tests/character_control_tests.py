from tests.conftest             import controls
from factories.factories        import CharacterControlFactory
from models.actors              import Actor
from controls.character_control import CharacterController

def test_read_in(controls:CharacterControlFactory):
    for character, controller in controls.characters.items():
        assert isinstance(character, Actor)
        assert isinstance(controller, CharacterController)
    assert controls.playable_characters() > 0