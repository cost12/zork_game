from utils.relator       import NameFinder
from models.actors       import Skill

def test_read_in(name_space:NameFinder):
    all = name_space.get_from_name(category='skill')
    for skill in all:
        assert isinstance(skill, Skill)
        for alias in skill.get_aliases():
            assert skill == name_space.get_from_name(alias, category='skill')[0]