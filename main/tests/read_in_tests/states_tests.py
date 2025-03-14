from tests.conftest      import states
from factories.factories import StateFactory
from models.state        import State
from models.action       import Action

def test_read_in(states:StateFactory):
    factory = states
    all = factory.get_states()
    for state in all:
        assert isinstance(state, State)
        assert state == factory.get_state(state.get_name())
        for action in state.get_actions_as_actor():
            assert isinstance(action, Action)
        for action in state.get_actions_as_target():
            assert isinstance(action, Action)
        for action in state.get_actions_as_tool():
            assert isinstance(action, Action)