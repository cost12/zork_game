from utils.relator       import NameFinder
from models.actors       import Action
from models.state        import State, StateGraph, StateGroup

def test_read_in(setup_space:NameFinder):
    all = setup_space.get_from_name(category='stategraph')
    for state_graph in all:
        assert isinstance(state_graph, StateGraph)
        for alias in state_graph.get_aliases():
            assert state_graph == setup_space.get_from_name(alias, category='stategraph')[0]
        for action in state_graph.get_available_actions_as_actor():
            assert isinstance(action, Action)
        for action in state_graph.get_available_actions_as_target():
            assert isinstance(action, Action)
        for action in state_graph.get_available_actions_as_tool():
            assert isinstance(action, Action)
        for state in state_graph.get_current_states():
            assert isinstance(state, State)
        for group, group_dict in state_graph.actor_graph.items():
            assert isinstance(group, StateGroup)
            for state in group.states:
                assert isinstance(state, State)
            for action, group2 in group_dict.items():
                assert isinstance(action, Action)
                assert isinstance(group2, StateGroup)
                for state2 in group2.states:
                    assert isinstance(state2, State)