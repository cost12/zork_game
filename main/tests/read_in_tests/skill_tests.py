from tests.conftest      import skills
from factories.factories import NamedFactory
from models.actors          import Skill

def test_read_in(skills:NamedFactory[Skill]):
    factory = skills
    all = factory.get_all_named()
    for skill in all:
        assert isinstance(skill, Skill)
        for alias in skill.get_aliases():
            assert skill == factory.get_named(alias)