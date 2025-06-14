from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.actors import Actor, Target, HasLocation
    from models.state  import State, Achievement
from models.response   import ResponseString

class ActionRequirement():
    def meets_requirement(self, character:'Actor') -> tuple[bool,ResponseString]:
        pass

    def _check_every_turn(self, character:'Actor') -> None:
        pass

class HappenedRequirement(ActionRequirement):
    def __init__(self, requirement:ActionRequirement, *, yes_response:ResponseString=None, no_response:ResponseString=None):
        self.requirement = requirement
        self.already_happened = set['Actor']()
        self.yes_response = yes_response
        self.no_response = no_response

    def _check_every_turn(self, character:'Actor') -> None:
        if self.requirement.meets_requirement(character):
            self.already_happened.add(character)

    def meets_requirement(self, character:'Actor') -> tuple[bool,ResponseString]:
        # TODO: how do I check this every turn - idea 1: make requirement item state -> don't need character, idea 2: check for each character
        if character in self.already_happened:
            return True, self.yes_response
        if self.requirement.meets_requirement(character):
            self.already_happened.add(character)
            return True, self.yes_response
        return False, self.no_response

class CharacterStateRequirement(ActionRequirement):
    def __init__(self, states_needed:dict['State',tuple[bool,ResponseString]]):
        self.states_needed = states_needed

    def meets_requirement(self, character:'Actor') -> tuple[bool,ResponseString]:
        for state, tup in self.states_needed.items():
            needed, response = tup
            if not (state in character.get_current_state()) == needed:
                return False, response
        return True, None
    
class CharacterAchievementRequirement(ActionRequirement):
    def __init__(self, achievements_needed:dict['Achievement',tuple[bool,ResponseString]]):
        self.achievements_needed = achievements_needed

    def meets_requirement(self, character:'Actor') -> tuple[bool,ResponseString]:
        for achievement, tup in self.achievements_needed.items():
            needed, response = tup
            if not character.has_completed_achievement(achievement) == needed:
                return False, response
        return True, None
    
class ItemStateRequirement(ActionRequirement):
    def __init__(self, item_states:dict['Target',dict['State',tuple[bool,ResponseString]]]):
        self.item_states_needed = item_states

    def meets_requirement(self, character:'Actor') -> tuple[bool,ResponseString]:
        for item, states_needed in self.item_states_needed.items():
            for state, tup in states_needed.items():
                needed, response = tup
                if not (state in item.get_current_state()) == needed:
                    return False, response
        return True, None
    
class ItemsHeldRequirement(ActionRequirement):
    def __init__(self, items_needed:dict['Target',tuple[bool,ResponseString]]):
        self.items_needed = items_needed

    def meets_requirement(self, character:'Actor') -> tuple[bool,ResponseString]:
        for item, tup in self.items_needed.items():
            needed, response = tup
            if not character.contains_item(item) == needed:
                return False, response
        return True, None
    
class WearingRequirement(ActionRequirement):
    def __init__(self, items_needed:dict['Target',tuple[bool,ResponseString]]):
        self.items_needed = items_needed

    def meets_requirement(self, character:'Actor') -> tuple[bool,ResponseString]:
        for item, tup in self.items_needed.items():
            needed, response = tup
            if not character.is_wearing(item) == needed:
                return False, response
        return True, None
    
class ItemPlacementRequirement(ActionRequirement):
    def __init__(self, item_placements:dict['Target',list[tuple['HasLocation',bool,ResponseString]]]):
        self.item_placements = item_placements

    def meets_requirement(self, character:'Actor'):
        for item, placement_info in self.item_placements.items():
            for location, needed, response in placement_info:
                if not (item.is_in(location) == needed):
                    return False, response
        return True, None
