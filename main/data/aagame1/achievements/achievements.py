from utils.relator import NameFinder
from models.state import Achievement

def add_to_name_space(name_space:NameFinder) -> None:
    achievement_inputs = [
        {"name" : "score"},
        {"name" : "gift skateboard to child"}
    ]

    achievements = [Achievement(**inputs) for inputs in achievement_inputs]

    name_space.add_many(achievements)