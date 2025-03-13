from tests.test_constants        import GAME_TO_TEST
from factories.data_read_in import read_in_directions
from factories.factories    import NamedFactory
from models.actors          import Direction

def test_read_in():
    direction_factory = read_in_directions(GAME_TO_TEST)
    all = direction_factory.get_all_named()
    for direction in all:
        assert isinstance(direction, Direction)
        for alias in direction.get_aliases():
            assert direction == direction_factory.get_named(alias)
    