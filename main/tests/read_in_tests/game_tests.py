from typing import Any

from factories.factories import LocationFactory, CharacterFactory, CharacterControlFactory, ItemFactory, NamedFactory
from models.action import Action
from models.actors import Direction
from tests.conftest import game

def test_read_in(game:tuple[LocationFactory, CharacterFactory, CharacterControlFactory, ItemFactory, NamedFactory[Action], NamedFactory[Direction], dict[str,Any]]):
    assert isinstance(game, tuple)
    assert isinstance(game[0], LocationFactory)
    assert isinstance(game[1], CharacterFactory)
    assert isinstance(game[2], CharacterControlFactory)
    assert isinstance(game[3], ItemFactory)
    assert isinstance(game[4], NamedFactory)
    assert isinstance(game[5], NamedFactory)
    assert isinstance(game[6], dict)
