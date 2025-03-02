from typing import Optional

from code.models.action import Action

class Item:
    """Base class for all Items/ anything that a Character can put in their Inventory
    """
    def __init__(self, name:str, description:str, weight:float, value:float, actions:Optional[list[Action]]=None):
        """Creates an Item

        :param name: The name of the Item
        :type name: str
        :param description: A description of the Item
        :type description: str
        :param weight: The weight of the Item
        :type weight: float
        :param value: The value of the Item
        :type value: float
        :param actions: Actions that can be performed with this item
        :type actions: list
        """
        self.name = name
        self.description = description
        self.weight = weight
        self.value = value
        self.actions = list[Action]() if actions is None else actions

    def get_name(self) -> str:
        """Gets the name of the Item

        :return: The name of the Item
        :rtype: str
        """
        return self.name

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
    
class Inventory:
    """Stores a Character's Items
    """
    def __init__(self, item_limit:int, weight_limit:float, items:Optional[list[tuple[Item,int]]]=None):
        """Creates an Inventory

        :param item_limit: The number of items the inventory can hold
        :type item_limit: int
        :param weight_limit: The total weight of items the inventory can hold
        :type weight_limit: float
        :param items: A list of initial Items in the inventory, defaults to None
        :type items: list[tuple[Item,int]], optional
        """
        self.item_limit = item_limit
        self.weight_limit = weight_limit
        assert items is None or (len(items) <= self.item_limit and sum([item[0].get_weight()*item[1] for item in items]) <= self.weight_limit)
        self.items = list[tuple[Item,int]]() if items is None else items

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
        return sum([item[0].get_value()*item[1] for item in self.items])
    
    def get_total_weight(self) -> float:
        """Gets the total weight of all Items in the Inventory

        :return: The total weight of all Items in the Inventory
        :rtype: float
        """
        return sum([item[0].get_weight()*item[1] for item in self.items])
    
    def add_item(self, item:Item, count:int=1) -> int:
        """If one or more of the Items can fit in the inventory, this adds the Items and returns the number that were added. Otherwise it returns 0.

        :param item: The Item to add to the Inventory
        :type item: Item
        :param count: The number of items to add to the Inventory, defaults to 1
        :type count: int, optional
        :return: The number of Items added
        :rtype: int
        """
        if len(self.items) < self.item_limit:
            space = self.weight_limit - self.get_total_weight()
            max_to_add = space / item.get_weight()
            to_add = min(max_to_add,count)
            if to_add > 0:
                self.items.append((item,to_add))
            return to_add
        return 0
    
    def drop_item(self, item:Item) -> bool:
        """If the Item is in the Inventory, this removes it and returns True. Otherwise it returns False.

        :param item: The Item to remove
        :type item: Item
        :return: True if the Item was removed, False if the Item was never in the Inventory
        :rtype: bool
        """
        i = 0
        for item2,count in self.items:
            if item == item2:
                if count > 1:
                    self.items[i][1] -= 1
                    return True
                else:
                    self.items.pop(i)
                    return True
            i += 1
        return False
