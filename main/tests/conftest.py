import pytest
from typing import Any

from utils.relator          import NameFinder
from factories.factories    import CharacterControlFactory
from factories.data_read_in import read_in_game

from tests.test_constants import GAME_TO_TEST

@pytest.fixture
def game() -> tuple[NameFinder, NameFinder, CharacterControlFactory, dict[str,Any]]:
    return read_in_game(GAME_TO_TEST)

@pytest.fixture
def name_space(game) -> NameFinder:
    return game[0]

@pytest.fixture
def setup_space(game) -> NameFinder:
    return game[1]

@pytest.fixture
def character_control(game) -> NameFinder:
    return game[2]

@pytest.fixture
def game_details(game) -> NameFinder:
    return game[3]