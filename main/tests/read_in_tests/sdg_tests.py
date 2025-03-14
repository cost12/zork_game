from tests.conftest      import state_disconnected_graphs
from factories.factories import StateDisconnectedGraphFactory
from models.state        import StateGraph, StateDisconnectedGraph

def test_read_in(state_disconnected_graphs:StateDisconnectedGraphFactory):
    factory = state_disconnected_graphs
    all = factory.get_state_disconnected_graphs()
    for sdg in all:
        assert isinstance(sdg, StateDisconnectedGraph)
        for alias in sdg.get_aliases():
            assert sdg == factory.get_state_disconnected_graph(alias)
        for graph in sdg.state_graphs:
            assert isinstance(graph, StateGraph)