from tests.conftest      import directions
from models.actors       import Direction
from factories.factories import NamedFactory

def test_read_in(directions:NamedFactory[Direction]):
    direction_factory = directions
    all = direction_factory.get_all_named()
    for direction in all:
        assert isinstance(direction, Direction)
        for alias in direction.get_aliases():
            assert direction == direction_factory.get_named(alias)
    