from utils.relator import NameFinder
from models.state import Skill

def add_to_name_space(name_space:NameFinder) -> None:
    skill_inputs = [
        {"name" : "strength"}
    ]

    skills = [Skill(**inputs) for inputs in skill_inputs]

    name_space.add_many(skills)
