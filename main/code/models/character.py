from typing import Optional

from code.models.actors import Actor
from code.models.item   import Inventory, Item
from code.models.state  import StateDisconnectedGraph, SkillSet, State, LocationDetail
from code.models.action import Action

class Character(Actor):
    """Base class for all Characters, user controlled or NPCs
    """
    def __init__(self, 
                 name:str, 
                 description:str,
                 type:str,
                 states:StateDisconnectedGraph, 
                 skills:SkillSet, 
                 inventory:Inventory,
                 actor_responses:Optional[dict[Action,str]]=None, 
                 target_responses:Optional[dict[Action,str]]=None, 
                 tool_responses:Optional[dict[Action,str]]=None,
                 state_responses:Optional[dict[State,str]]=None,
                 aliases:Optional[list[str]]=None):
        super().__init__(name, description, states, skills, actor_responses, target_responses, tool_responses, state_responses, aliases)
        self.type = type
        self.inventory = inventory
        self.inventory_location = LocationDetail(f"{self.name}'s inventory", True, hidden=True)

    def get_type(self) -> str:
        """Gets the Character's type

        :return: The Character's type
        :rtype: str
        """
        return self.type

    def _set_location(self, location, detail, *, origin=False):
        super()._set_location(location, detail, origin=origin)
        for item in self.inventory.get_items():
            item.change_location(location, self.inventory_location)

    def get_inventory_weight(self) -> float:
        return self.inventory.get_total_weight()
    
    def get_inventory_value(self) -> float:
        return self.inventory.get_total_value()
    
    def get_inventory_size(self) -> float:
        return self.inventory.get_total_size()
    
    def add_item_to_inventory(self, item:Item) -> bool:
        if self.inventory.add_item(item):
            item.change_location(self.location, self.inventory_location)
            return True
        return False
    
    def remove_item_from_inventory(self, item:Item) -> bool:
        if self.inventory.drop_item(item):
            item.change_location(self.location)
            return True
        return False
    
    def get_inventory_items(self) -> list[Item]:
        return self.inventory.get_items()
    
    def is_holding(self, item:Item) -> bool:
        return self.inventory.contains(item)