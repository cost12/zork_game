from tests.conftest      import items
from factories.factories import ItemFactory
from models.item         import Item
from models.action       import Action
from models.state        import State, FullState

def test_read_in(items:ItemFactory):
    factory = items
    all = factory.get_items()
    for item in all:
        assert isinstance(item, Item)
        assert isinstance(item.weight, float) or isinstance(item.weight, int)
        assert isinstance(item.value,  float) or isinstance(item.value, int)
        assert isinstance(item.size,   float) or isinstance(item.size, int)
        assert isinstance(item.description, str)
        assert isinstance(item.states, FullState)
        for state, response in item.state_responses.items():
            assert isinstance(state, State)
            assert isinstance(response, str)
        for action, response in item.target_responses.items():
            assert isinstance(action, Action)
            assert isinstance(response, str)
        for action, response in item.tool_responses.items():
            assert isinstance(action, Action)
            assert isinstance(response, str)
        for alias in item.get_aliases():
            assert item == factory.get_item(alias)