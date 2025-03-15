import pytest
from typing import Any

from models.action          import Action
from models.actors          import Direction
from models.state           import Skill
from factories.factories    import NamedFactory, StateFactory, StateGraphFactory, StateDisconnectedGraphFactory, ItemFactory, SkillSetFactory, CharacterFactory, LocationFactory, CharacterControlFactory
from factories.data_read_in import read_in_directions, read_in_actions, read_in_skills, read_in_states, read_in_state_graphs, read_in_state_disconnected_graphs, read_in_items, read_in_skill_sets, read_in_characters, read_in_rooms, read_in_character_control, read_in_game_details, read_in_game

from tests.test_constants import GAME_TO_TEST

@pytest.fixture
def directions() -> NamedFactory[Direction]:
    return read_in_directions(GAME_TO_TEST)

@pytest.fixture
def actions() -> NamedFactory[Action]:
    return read_in_actions(GAME_TO_TEST)

@pytest.fixture
def states(actions:NamedFactory[Action]) -> StateFactory:
    return read_in_states(GAME_TO_TEST, actions)

@pytest.fixture
def state_graphs(states:StateFactory, actions:NamedFactory[Action]) -> StateGraphFactory:
    return read_in_state_graphs(GAME_TO_TEST, states, actions)

@pytest.fixture
def state_disconnected_graphs(state_graphs:StateGraphFactory) -> StateDisconnectedGraphFactory:
    return read_in_state_disconnected_graphs(GAME_TO_TEST, state_graphs)

@pytest.fixture
def items(state_disconnected_graphs:StateDisconnectedGraphFactory, actions:NamedFactory[Action], states:StateFactory) -> ItemFactory:
    return read_in_items(GAME_TO_TEST, state_disconnected_graphs, actions, states)

@pytest.fixture
def skills() -> NamedFactory[Skill]:
    return read_in_skills(GAME_TO_TEST)

@pytest.fixture
def skill_sets(skills:NamedFactory[Skill]) -> SkillSetFactory:
    return read_in_skill_sets(GAME_TO_TEST, skills)

@pytest.fixture
def characters(state_disconnected_graphs:StateDisconnectedGraphFactory, skill_sets:SkillSetFactory, items:ItemFactory, actions:NamedFactory[Action], states:StateFactory) -> CharacterFactory:
    return read_in_characters(GAME_TO_TEST, state_disconnected_graphs, skill_sets, items, actions, states)

@pytest.fixture
def rooms(characters:CharacterFactory, items:ItemFactory, directions:NamedFactory[Direction], states:StateFactory) -> LocationFactory:
    return read_in_rooms(GAME_TO_TEST, characters, items, directions, states)

@pytest.fixture
def controls(characters:CharacterFactory) -> CharacterControlFactory:
    return read_in_character_control(GAME_TO_TEST, characters)

@pytest.fixture
def game_details() -> dict[str,Any]:
    return read_in_game_details(GAME_TO_TEST)

@pytest.fixture
def game() -> tuple[LocationFactory, CharacterFactory, CharacterControlFactory, ItemFactory, NamedFactory[Action], NamedFactory[Direction], dict[str,Any]]:
    return read_in_game(GAME_TO_TEST)

# Test
@pytest.fixture
def test_directions() -> NamedFactory[Direction]:
    return read_in_directions('test_game')

@pytest.fixture
def test_actions() -> NamedFactory[Action]:
    return read_in_actions('test_game')

@pytest.fixture
def test_states(actions:NamedFactory[Action]) -> StateFactory:
    return read_in_states('test_game', actions)

@pytest.fixture
def test_state_graphs(states:StateFactory, actions:NamedFactory[Action]) -> StateGraphFactory:
    return read_in_state_graphs('test_game', states, actions)

@pytest.fixture
def test_state_disconnected_graphs(state_graphs:StateGraphFactory) -> StateDisconnectedGraphFactory:
    return read_in_state_disconnected_graphs('test_game', state_graphs)

@pytest.fixture
def test_items(state_disconnected_graphs:StateDisconnectedGraphFactory, actions:NamedFactory[Action], states:StateFactory) -> ItemFactory:
    return read_in_items('test_game', state_disconnected_graphs, actions, states)

@pytest.fixture
def test_skills() -> NamedFactory[Skill]:
    return read_in_skills('test_game')

@pytest.fixture
def test_skill_sets(skills:NamedFactory[Skill]) -> SkillSetFactory:
    return read_in_skill_sets('test_game', skills)

@pytest.fixture
def test_characters(state_disconnected_graphs:StateDisconnectedGraphFactory, skill_sets:SkillSetFactory, items:ItemFactory, actions:NamedFactory[Action], states:StateFactory) -> CharacterFactory:
    return read_in_characters('test_game', state_disconnected_graphs, skill_sets, items, actions, states)

@pytest.fixture
def test_rooms(characters:CharacterFactory, items:ItemFactory, directions:NamedFactory[Direction], states:StateFactory) -> LocationFactory:
    return read_in_rooms('test_game', characters, items, directions, states)

@pytest.fixture
def test_controls(characters:CharacterFactory) -> CharacterControlFactory:
    return read_in_character_control('test_game', characters)

@pytest.fixture
def test_game_details() -> dict[str,Any]:
    return read_in_game_details('test_game')

@pytest.fixture
def test_game() -> tuple[LocationFactory, CharacterFactory, CharacterControlFactory, ItemFactory, NamedFactory[Action], NamedFactory[Direction], dict[str,Any]]:
    return read_in_game('test_game')