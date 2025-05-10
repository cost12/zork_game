from factories.factories        import CharacterControlFactory
from models.actors              import Actor
from controls.character_control import CharacterController

def test_read_in(character_control:CharacterControlFactory):
    for character, controller in character_control.characters.items():
        assert isinstance(character, Actor)
        assert isinstance(controller, CharacterController)
    assert character_control.playable_characters() > 0