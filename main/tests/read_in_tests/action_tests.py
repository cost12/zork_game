from utils.relator       import NameFinder
from models.actors       import Action

def test_read_in(name_space:NameFinder):
    all = name_space.get_from_name(category='action')
    for action in all:
        assert isinstance(action, Action)
        for alias in action.get_aliases():
            assert action == name_space.get_from_name(alias, category='action')[0]