from utils.relator       import NameFinder
from models.actors       import Target
from models.named        import Action
from models.state        import State, FullState
from models.response     import ResponseString

def test_read_in(name_space:NameFinder):
    all = name_space.get_from_name(category='target')
    for item in all:
        assert isinstance(item, Target)
        assert isinstance(item.weight, float) or isinstance(item.weight, int)
        assert isinstance(item.value,  float) or isinstance(item.value, int)
        assert isinstance(item.size,   float) or isinstance(item.size, int)
        assert isinstance(item.description, ResponseString)
        assert isinstance(item.states, FullState)
        for state, response in item.state_responses.items():
            assert isinstance(state, State)
            assert isinstance(response, ResponseString)
        for action, response in item.target_responses.items():
            assert isinstance(action, Action)
            assert isinstance(response, ResponseString)
        for action, response in item.tool_responses.items():
            assert isinstance(action, Action)
            assert isinstance(response, ResponseString)
        for alias in item.get_aliases():
            assert item == name_space.get_from_name(alias, category='target')[0]