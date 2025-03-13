from typing import Optional

from models.action import Action
from models.actors import Target
from models.state  import StateDisconnectedGraph

class Item(Target):
    """Base class for all Items/ anything that a Character can put in their Inventory
    """
    def __init__(self, 
                 name:str, 
                 description:str, 
                 states:StateDisconnectedGraph,
                 weight:float=1,
                 value:float=0,
                 size:float=1,
                 target_responses:Optional[dict[Action,str]]=None,
                 tool_responses:Optional[dict[Action,str]]=None,
                 state_responses:Optional[dict[Action,str]]=None):
        super().__init__(name, description, states, target_responses, tool_responses, state_responses)
        self.description = description
        self.weight = weight
        self.value = value
        self.size = size
        self.moved=False

    def get_weight(self) -> float:
        """Gets the weight of the Item

        :return: The weight of the Item
        :rtype: float
        """
        return self.weight

    def get_value(self) -> float:
        """Gets the value of the Item

        :return: The value of the Item
        :rtype: float
        """
        return self.value

    def get_size(self) -> float:
        return self.size

class Inventory:
    """Stores a Character's Items
    """
    def __init__(self, size_limit:int, weight_limit:float, items:Optional[list[Item]]=None):
        self.size_limit = size_limit
        self.weight_limit = weight_limit
        assert items is None or (sum([item.get_size() for item in items]) <= self.size_limit and sum([item.get_weight() for item in items]) <= self.weight_limit)
        self.items = list[Item]() if items is None else items

    def get_items(self) -> list[Item]:
        """Gets a list of Items in the Inventory

        :return: A list of Items in the Inventory
        :rtype: list[Item]
        """
        return self.items
    
    def get_total_value(self) -> float:
        """Gets the total value of all Items in the Inventory

        :return: The total value of all Items in the Inventory
        :rtype: float
        """
        return sum([item.get_value() for item in self.items])
    
    def get_total_weight(self) -> float:
        """Gets the total weight of all Items in the Inventory

        :return: The total weight of all Items in the Inventory
        :rtype: float
        """
        return sum([item.get_weight() for item in self.items])
    
    def get_total_size(self) -> float:
        """Gets the total size of all Items in the Inventory

        :return: The total size of all Items in the Inventory
        :rtype: float
        """
        return sum([item.get_size() for item in self.items])
    
    def contains(self, item:Item) -> bool:
        """Whether item is in the Inventory or not

        :param item: The Item to check
        :type item: Item
        :return: True if item is in the Inventory, False otherwise
        :rtype: bool
        """
        return item in self.items
    
    def add_item(self, item:Item) -> bool:
        """If one or more of the Items can fit in the inventory, this adds the Items and returns the number that were added. Otherwise it returns 0.

        :param item: The Item to add to the Inventory
        :type item: Item
        :return: True if successful
        :rtype: bool
        """
        if item.get_size() + self.get_total_size() <= self.size_limit and item.get_weight() + self.get_total_weight():
            self.items.append(item)
            return True
        return False
    
    def drop_item(self, item:Item) -> bool:
        """If the Item is in the Inventory, this removes it and returns True. Otherwise it returns False.

        :param item: The Item to remove
        :type item: Item
        :return: True if the Item was removed, False if the Item was never in the Inventory
        :rtype: bool
        """
        if item in self.items:
            self.items.remove(item)
            return True
        return False
