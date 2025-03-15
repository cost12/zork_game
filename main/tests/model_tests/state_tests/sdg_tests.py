from tests.conftest import test_state_disconnected_graphs, test_states, test_actions
from factories.factories import StateDisconnectedGraphFactory, StateGraphFactory, StateFactory, NamedFactory
from models.action import Action

def test_has_state(test_state_disconnected_graphs:StateDisconnectedGraphFactory, test_states:StateFactory):
    full_state = test_state_disconnected_graphs.get_state_disconnected_graph('standard_item')
    assert     full_state.has_state(test_states.get_state('not held'))
    assert     full_state.has_state(test_states.get_state('off'))
    assert     full_state.has_state(test_states.get_state('normal_item'))
    assert not full_state.has_state(test_states.get_state('broken_item'))
    assert not full_state.has_state(test_states.get_state('held'))

def test_current_states(test_state_disconnected_graphs:StateDisconnectedGraphFactory, test_states:StateFactory):
    graph = test_state_disconnected_graphs.get_state_disconnected_graph('standard_item')
    assert test_states.get_state('off') in graph.get_current_states()
    assert test_states.get_state('not held') in graph.get_current_states()
    for state in graph.get_current_states():
        assert graph.has_state(state)

def test_perform_action(test_state_disconnected_graphs:StateDisconnectedGraphFactory, test_actions:NamedFactory[Action], test_states:StateFactory):
    graph = test_state_disconnected_graphs.get_state_disconnected_graph('standard_item')
    assert graph.perform_action_as_target(test_actions.get_named('take')) == [test_states.get_state('held')]
    assert graph.perform_action_as_target(test_actions.get_named('take')) == []
    assert graph.perform_action_as_target(test_actions.get_named('drop')) == [test_states.get_state('not held')]
    assert graph.perform_action_as_target(test_actions.get_named('toggle')) == [test_states.get_state('on')]
    changes =  graph.perform_action_as_target(test_actions.get_named('break'))
    assert test_states.get_state('off') in changes
    assert test_states.get_state('broken_item') in changes