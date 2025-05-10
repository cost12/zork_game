from utils.relator       import NameFinder
from models.actors       import Location, LocationDetail, Target, Direction, Path

def test_read_in(name_space:NameFinder):
    all = name_space.get_from_name(category='location')
    for room in all:
        assert isinstance(room, Location)
        assert isinstance(room.start_location, bool)
        for alias in room.get_aliases():
            assert room == name_space.get_from_name(alias, category='location')[0]