from code.models.item import Item

from typing import Optional

class Inventory:
    """Stores a Character's Items
    """
    def __init__(self, item_limit:int, weight_limit:float, items:Optional[list[Item]]=None):
        """Creates an Inventory

        :param item_limit: The number of items the inventory can hold
        :type item_limit: int
        :param weight_limit: The total weight of items the inventory can hold
        :type weight_limit: float
        :param items: A list of initial Items in the inventory, defaults to None
        :type items: list[Item], optional
        """
        self.item_limit = item_limit
        self.weight_limit = weight_limit
        assert items is None or (len(items) <= self.item_limit and sum([item.get_weight() for item in items] <= self.weight_limit))
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
    
    def add_item(self, item:Item) -> bool:
        """If the Item can fit in the inventory, this adds the Item and returns True. Otherwise it returns False.

        :param item: The Item to add to the Inventory
        :type item: Item
        :return: True if the Item is added, False otherwise
        :rtype: bool
        """
        if len(self.items) < self.item_limit:
            if self.get_total_weight() + item.get_weight() < self.weight_limit:
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
        try:
            self.items.remove(item)
            return True
        except ValueError:
            return False

class Character:
    """Base class for all Characters, user controlled or NPCs
    """
    def __init__(self, name:str, type:str, inventory:Optional[Inventory]=None):
        """Creates a Character

        :param name: The Character's name
        :type name: str
        :param type: What type of being the character is ex. human, dragon, ...
        :type type: str
        :param inventory: The Character's initial Inventory, defaults to None
        :type inventory: Inventory, optional
        """
        self.name = name
        self.type = type
        self.inventory = Inventory(10,10) if inventory is None else inventory

    def get_name(self) -> str:
        """Gets the Character's name

        :return: The Character's name
        :rtype: str
        """
        return self.name

    def get_type(self) -> str:
        """Get's the Character's type

        :return: The Character's type
        :rtype: str
        """
        return self.type

    def get_inventory(self) -> list[Item]:
        """Gets the Character's inventory

        :return: The Character's inventory
        :rtype: Inventory
        """
        return self.inventory

