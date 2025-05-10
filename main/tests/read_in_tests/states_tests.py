from utils.relator       import NameFinder
from models.state        import State
from models.named        import Action

def test_read_in(name_space:NameFinder):
    all = name_space.get_from_name(category='state')
    for state in all:
        assert isinstance(state, State)
        assert state == name_space.get_from_name(state.get_name(), category='state')[0]
        for action in state.get_actions_as_actor():
            assert isinstance(action, Action)
        for action in state.get_actions_as_target():
            assert isinstance(action, Action)
        for action in state.get_actions_as_tool():
            assert isinstance(action, Action)