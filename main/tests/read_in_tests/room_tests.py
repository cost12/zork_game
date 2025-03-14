from tests.conftest      import rooms
from factories.factories import LocationFactory
from models.actors       import Location, LocationDetail, Target, Direction, Path, Actor
from models.action       import Action
from models.state        import State, FullState

def test_read_in(rooms:LocationFactory):
    factory = rooms
    all = factory.get_locations()
    for room in all:
        assert isinstance(room, Location)
        assert isinstance(room.start_location, bool)
        for alias in room.get_aliases():
            assert room == factory.get_location(alias)
        assert isinstance(room.description, str)
        for target, detail in room.contents.items():
            assert isinstance(target, Target)
            assert isinstance(detail, LocationDetail)
            assert (room, detail) == target.get_location()
            assert detail in room.details
        for detail in room.details:
            assert isinstance(detail, LocationDetail)
        for direction, response in room.direction_responses.items():
            assert isinstance(direction, Direction)
            assert isinstance(response, str)
        for direction, path in room.paths.items():
            assert isinstance(direction, Direction)
            assert isinstance(path, Path)
            assert isinstance(path.description, str)
            assert isinstance(path.end, Location)
            assert isinstance(path.hidden, bool)
            for target, state in path.linked_targets.items():
                assert isinstance(target, Target)
                assert isinstance(state, State)
            for actor, state in path.passing_requirements.items():
                assert isinstance(actor, Actor)
                assert isinstance(state, State)