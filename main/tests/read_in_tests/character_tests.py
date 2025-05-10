from models.actors       import Actor
from models.named        import Action
from models.state        import State, FullState, SkillSet
from utils.relator import NameFinder
from models.response    import ResponseString

def test_read_in(name_space:NameFinder):
    all = name_space.get_from_name(category='actor')
    for character in all:
        assert isinstance(character, Actor)
        assert isinstance(character.states, FullState)
        assert isinstance(character.description, ResponseString)
        assert isinstance(character.weight, float) or isinstance(character.weight, int)
        assert isinstance(character.size, float) or isinstance(character.size, int)
        assert isinstance(character.value, float) or isinstance(character.value, int)
        assert isinstance(character.type, str)
        assert isinstance(character.skills, SkillSet)
        for state, response in character.state_responses.items():
            assert isinstance(state, State)
            assert isinstance(response, ResponseString)
        for action, response in character.actor_responses.items():
            assert isinstance(action, Action)
            assert isinstance(response, ResponseString)
        for action, response in character.target_responses.items():
            assert isinstance(action, Action)
            assert isinstance(response, ResponseString)
        for action, response in character.tool_responses.items():
            assert isinstance(action, Action)
            assert isinstance(response, ResponseString)
        for alias in character.get_aliases():
            assert character == name_space.get_from_name(alias, category='actor')[0]