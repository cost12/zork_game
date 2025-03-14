from typing import Any

from tests.conftest import game_details

def test_read_in(game_details:dict[str,Any]):
    assert isinstance(game_details, dict)
    for string, _ in game_details.items():
        assert isinstance(string, str)