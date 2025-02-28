

class Item:
    """Base class for all Items/ anything that a Character can put in their Inventory
    """
    def __init__(self, name:str, weight:float, value:float):
        """Creates an Item

        :param name: The name of the Item
        :type name: str
        :param weight: The weight of the Item
        :type weight: float
        :param value: The value of the Item
        :type value: float
        """
        self.name = name
        self.weight = weight
        self.value = value

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
    
