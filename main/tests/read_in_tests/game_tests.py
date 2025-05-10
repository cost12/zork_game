from typing import Any

from factories.factories import CharacterControlFactory
from utils.relator       import NameFinder

def test_read_in(game:tuple[NameFinder, NameFinder, CharacterControlFactory, dict[str,Any]]):
    assert isinstance(game, tuple)
    assert isinstance(game[0], NameFinder)
    assert isinstance(game[1], NameFinder)
    assert isinstance(game[2], CharacterControlFactory)
    assert isinstance(game[3], dict)
