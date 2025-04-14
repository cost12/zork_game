from tests.conftest      import characters
from factories.factories import CharacterFactory
from models.actors       import Actor, LocationDetail
from models.named        import Action
from models.state        import State, FullState, SkillSet

def test_read_in(characters:CharacterFactory):
    factory = characters
    all = factory.get_characters()
    for character in all:
        assert isinstance(character, Actor)
        assert isinstance(character.states, FullState)
        assert isinstance(character.description, str)
        assert isinstance(character.weight, float) or isinstance(character.weight, int)
        assert isinstance(character.size, float) or isinstance(character.size, int)
        assert isinstance(character.value, float) or isinstance(character.value, int)
        assert isinstance(character.type, str)
        assert isinstance(character.skills, SkillSet)
        for state, response in character.state_responses.items():
            assert isinstance(state, State)
            assert isinstance(response, str)
        for action, response in character.actor_responses.items():
            assert isinstance(action, Action)
            assert isinstance(response, str)
        for action, response in character.target_responses.items():
            assert isinstance(action, Action)
            assert isinstance(response, str)
        for action, response in character.tool_responses.items():
            assert isinstance(action, Action)
            assert isinstance(response, str)
        for alias in character.get_aliases():
            assert character == factory.get_character(alias)