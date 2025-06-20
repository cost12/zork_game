from utils.relator import NameFinder
from models.actors import Target, Actor, Location, LocationDetail, Path

class StandIn[T]:
    def __init__(self, id:str, category:str):
        self.id = id
        self.category = category

    def get_from_name_space(self, name_space:NameFinder) -> T:
        return name_space.get_from_id(self.id, self.category)
    
def replace_standins_item(item:Target, name_space:NameFinder) -> None:
    pass

def replace_standins_character(character:Actor, name_space:NameFinder) -> None:
    pass

def replace_standins_location_detail(location_detail:LocationDetail, name_space:NameFinder) -> None:
    pass

def replace_standins_path(path:Path, name_space:NameFinder) -> None:
    pass

def replace_standins_location(location:Location, name_space:NameFinder) -> None:
    pass

def replace_standins(name_space:NameFinder) -> None:
    for item in name_space.get_from_name(category="target"):
        replace_standins_item(item, name_space)
    for character in name_space.get_from_name(category="actor"):
        replace_standins_character(character, name_space)
    for location_detail in name_space.get_from_name(category="locationdetail"):
        replace_standins_location_detail(location_detail, name_space)
    for path in name_space.get_from_name(category=["singleendpath", "multiendpath"]):
        replace_standins_path(path, name_space)
    for location in name_space.get_from_name(category="location"):
        replace_standins_location(location, name_space)
