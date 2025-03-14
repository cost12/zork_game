from tests.conftest      import actions
from factories.factories import NamedFactory
from models.actors       import Action

def test_read_in(actions:NamedFactory[Action]):
    factory = actions
    all = factory.get_all_named()
    for action in all:
        assert isinstance(action, Action)
        for alias in action.get_aliases():
            assert action == factory.get_named(alias)