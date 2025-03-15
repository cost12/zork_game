from tests.conftest import test_state_graphs, test_states, test_actions
from factories.factories import StateGraphFactory, StateFactory, NamedFactory
from models.action import Action

def test_has_state(test_state_graphs:StateGraphFactory, test_states:StateFactory):
    graph = test_state_graphs.get_state_graph('standard_item')
    assert     graph.has_state(test_states.get_state('normal_item'))
    assert not graph.has_state(test_states.get_state('broken_item'))

def test_current_states(test_state_graphs:StateGraphFactory, test_states:StateFactory):
    graph = test_state_graphs.get_state_graph('switch')
    assert graph.get_current_states() == [test_states.get_state('off')]
    for state in graph.get_current_states():
        assert graph.has_state(state)

def test_perform_action(test_state_graphs:StateGraphFactory, test_actions:NamedFactory[Action], test_states:StateFactory):
    graph = test_state_graphs.get_state_graph('switch')
    assert test_actions.get_named('toggle') in graph.get_available_actions_as_target()
    assert graph.perform_action_as_target(test_actions.get_named('toggle'))  == [test_states.get_state('on')]
    assert graph.perform_action_as_target(test_actions.get_named('toggle'))  == [test_states.get_state('off')]
    assert graph.perform_action_as_target(test_actions.get_named('turn on')) == [test_states.get_state('on')]
    assert graph.perform_action_as_target(test_actions.get_named('break'))   == [test_states.get_state('off')]
    assert graph.perform_action_as_target(test_actions.get_named('toggle'))  == []
    assert graph.perform_action_as_target(test_actions.get_named('turn on')) == []