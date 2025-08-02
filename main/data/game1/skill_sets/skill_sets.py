from utils.relator import NameFinder
from models.state import SkillSet

def add_to_name_space(name_space:NameFinder) -> None:
    skill_sets = [
        SkillSet(
            name="standard",
            skills={
                name_space.get_from_id("strength", "skill") : 0
            },
            default_proficiency=0
        )
    ]

    name_space.add_many(skill_sets)
