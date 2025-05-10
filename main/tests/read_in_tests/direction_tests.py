from models.actors       import Direction
from utils.relator       import NameFinder


def test_read_in(name_space:NameFinder):
    all = name_space.get_from_name(category='direction')
    for direction in all:
        assert isinstance(direction, Direction)
        for alias in direction.get_aliases():
            assert direction == name_space.get_from_name(alias, category='direction')[0]