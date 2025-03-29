from typing import Optional

from models.action import Named

# Get for entering State?
# For doing Action with Item/ in room

class Achievement(Named):
    
    def __init__(self, name:str, description:str, *, aliases:Optional[str]=None):
        super().__init__(name, aliases)
        self.description = description