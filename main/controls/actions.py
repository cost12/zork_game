from dataclasses import dataclass
from enum        import Enum

from models.actors              import Target, NamedContainer, World
from models.named               import Action, Direction, ActionContext, Named
from controls.character_control import Feedback
from readin.description_helpers import Description, DescriptionContext, ContentsContext, ContentsDescription, \
                                       plain_text_description, combine_descriptions, backup_description
from readin.restriction_helpers import RestrictionContext

@dataclass
class LookContext:
    target : NamedContainer|None = None

class LookAction(Action[LookContext]):

    def check_inputs(self, inputs) -> tuple[bool,LookContext,Description]:
        if len(inputs) == 0:
            return True, LookContext(), None
        if len(inputs) == 1:
            if isinstance(inputs[0], NamedContainer):
                return True, LookContext(inputs[0]), None
            return False, None, plain_text_description("You can't look at that.")
        return False, None, plain_text_description("Pick something to focus on.")

    def take_action(self, current_state:World, context:ActionContext, inputs:LookContext) -> Feedback:
        if inputs.target:
            can_look, r = current_state.can_act_on(context.character, inputs.target, self)
            response = [r]
            if can_look:
                response.append(context.character.perform_action_as_actor(self))
                if isinstance(inputs.target, Target):
                    response.append(inputs.target.perform_action_as_target(self))
                response.append(inputs.target.describe(RestrictionContext(context.character, current_state.item_locations)))
        else:
            can_look, r = current_state.can_act(context.character, self)
            response = [r]
            if can_look:
                response.append(context.character.perform_action_as_actor(self))
                room = current_state.get_room(context.character)
                response.append(
                    current_state.describe_room(
                        room,
                        RestrictionContext(context.character, current_state.get_local_tree(context.character))
                    )
                )
        return Feedback(
            description =combine_descriptions(response),
            context     =DescriptionContext(
                placements =current_state.item_locations,
                action     =self,
                success    =can_look,
                character  =context.character,
                target     =inputs.target,
                tool       =None
            ),
            moves =1,
            turns =0,
            score =0
        )

class WalkAction(Action[Direction]):

    def check_inputs(self, inputs:tuple) -> tuple[bool,Direction,Description]:
        if len(inputs) == 1:
            if isinstance(inputs[0], Direction):
                return True, inputs, None
            return False, None, plain_text_description("What direction?")
        if len(inputs) == 0:
            return False, None, plain_text_description("What direction?")
        return False, None, plain_text_description("That's a lot of words. Which way do you want to go?")

    def take_action(self, current_state:World, context:ActionContext, inputs:Direction) -> Feedback:
        direction = inputs
        response = list[Description]()
        can_walk, r = current_state.can_act(context.character, self)
        look_action = LookAction("look")
        can_see, _ = current_state.can_act(context.character, action=look_action)
        success=False
        if not can_see:
            response.append(plain_text_description("You fumble around in the darkness blindly, finally finding an exit."))
            direction = Direction("random")
        response.append(r)
        if can_walk:
            success, r = current_state.walk(context.character, direction)
            if success:
                response.append(r)
                response.append(context.character.perform_action_as_actor(self))
                response.append(look_action.take_action(current_state, context, LookContext(None))[1])
            else:
                response.append(backup_description([r, plain_text_description("You are unable to exit.")]))
        return Feedback(
            description=combine_descriptions(response),
            context=DescriptionContext(
                placements =current_state.item_locations,
                action     =self,
                success    =success,
                character  =context.character,
                target     =None,
                tool       =None
            ),
            moves=1,
            turns=int(success),
            score=0
        )

class WaitAction(Action[tuple]):

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,Description]:
        if len(inputs) == 0:
            return True, tuple(), None
        return False, tuple(), plain_text_description("Thats a lot of words. Do you want to wait?")

    def take_action(self, current_state:World, context:ActionContext, inputs:tuple):
        response = []
        can_wait, r = current_state.can_act(context.character, self)
        response.append(r)
        if can_wait:
            response.append(backup_description([context.character.perform_action_as_actor(self), plain_text_description("Time passes.")]))
        return Feedback(
            description=combine_descriptions(response),
            context=DescriptionContext(
                placements =current_state.item_locations,
                action     =self,
                success    =can_wait,
                character  =context.character,
                target     =None,
                tool       =None
            ),
            moves=1,
            turns=int(can_wait),
            score=0
        )

@dataclass
class TakeContext:
    targets : list[Target]

class InventoryType(Enum):
    INVENTORY = 0
    WEARING   = 1

@dataclass
class TakeAction(Action[TakeContext]):
    inventory       : InventoryType = InventoryType.INVENTORY
    cant_take_text  : str           = "You can't take that."
    empty_take_text : str           = "Your inventory is empty."
    full_pack_text  : str           = "Your inventory is full."
    taken_text      : str           = "Taken."
    not_taken_text  : str           = "No items were taken."

    def check_inputs(self, inputs:tuple[Named]) -> tuple[bool,TakeContext,Description]:
        for i in inputs:
            if not isinstance(i, Target):
                return False, None, plain_text_description(f"{self.cant_take_text} {i.get_name()}!")
        if len(inputs) > 0:
            return True, TakeContext(list(inputs)), None
        return False, None, plain_text_description(self.empty_take_text)

    def take_action(self, current_state:World, context:ActionContext, inputs:TakeContext) -> Feedback:
        response = []
        success = False
        target=None
        for target in inputs.targets:
            can_be_taken, r = current_state.can_act_on(context.character, target, self)
            response.append(r)
            if can_be_taken:
                match self.inventory:
                    case InventoryType.INVENTORY:
                        inventory = context.character.get_inventory()
                    case InventoryType.WEARING:
                        inventory = context.character.get_wearing()
                added, r = current_state.move_item(target, inventory)
                response.append(r)
                if added:
                    success = True
                    response.append(target.perform_action_as_target(self))
                else:
                    response.append(plain_text_description(f"{target.get_name()} {self.full_pack_text}"))
        if success:
            response.append(plain_text_description(self.taken_text))
            response.append(context.character.perform_action_as_actor(self))
        else:
            response.append(plain_text_description(self.not_taken_text))
        return Feedback(
            description=combine_descriptions(response),
            context=DescriptionContext(
                placements =current_state.item_locations,
                action     =self,
                success    =success,
                character  =context.character,
                target     =inputs.targets,
                tool       =None
            ),
            moves=1,
            turns=int(success),
            score=0
        )

@dataclass
class DropContext:
    targets   : list[Target]
    placement : NamedContainer|None = None

@dataclass
class DropAction(Action[DropContext]):
    inventory       :InventoryType = InventoryType.INVENTORY
    cant_drop_text  :str           = "You can't drop that."
    empty_drop_text :str           = "You have nothing to drop."
    dropped_text    :str           = "Dropped."
    no_drop_text    :str           = "No items were dropped."

    def check_inputs(self, inputs:tuple[Named]) -> tuple[bool,DropContext,Description]:
        targets = []
        placement = None
        for i in inputs:
            if isinstance(i, Target):
                targets.append(i)
            elif isinstance(i, tuple) and i[0] == 'placement':
                placement = i[1]
            else:
                return False, None, plain_text_description(f"{self.cant_drop_text} {i.get_name()}!")
        if len(inputs) > 0:
            return True, DropContext(targets, placement), None
        return False, None, plain_text_description(self.empty_drop_text)

    def take_action(self, current_state:World, context:ActionContext, inputs:DropContext) -> Feedback:
        response = []
        success = False
        target=None
        for target in inputs.targets:
            can_be_dropped, r = current_state.can_act_on(context.character, target, self)
            response.append(r)
            if can_be_dropped:
                if inputs.placement is None:
                    placement = current_state.get_room(context.character)
                else:
                    placement = inputs.placement
                dropped, r = current_state.move_item(target, placement)
                response.append(r)
                if dropped:
                    success = True
                    response.append(target.perform_action_as_target(self))
        if success:
            response.append(plain_text_description(self.dropped_text))
            response.append(context.character.perform_action_as_actor(self))
        else:
            response.append(plain_text_description(self.no_drop_text))
        return Feedback(
            description=combine_descriptions(response),
            context=DescriptionContext(
                placements =current_state.item_locations,
                action     =self,
                success    =success,
                character  =context.character,
                target     =inputs.targets,
                tool       =None
            ),
            moves=1,
            turns=int(success),
            score=0
        )

@dataclass
class CheckInventoryAction(Action[tuple]):
    inventory     :InventoryType = InventoryType.INVENTORY
    contains_text :str           = "Your inventory contains:"
    empty_text    :str           = "Your inventory is empty."

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,Description]:
        if len(inputs) == 0:
            return True, tuple(), None
        return False, None, plain_text_description("That's a lot of words.")

    def take_action(self, current_state:World, context:ActionContext, inputs:tuple) -> Feedback:
        response = []
        can_check, r = current_state.can_act(context.character, self)
        response.append(r)
        if can_check:
            response.append(Description[ContentsContext](
                context.character,
                ContentsContext(
                    plain_text_description(f"{self.contains_text}:\n\t"),
                    plain_text_description(f"{self.empty_text}")
                ),
                ContentsDescription()
            ))
        return Feedback(
            description=combine_descriptions(response),
            context=DescriptionContext(
                placements =current_state.item_locations,
                action     =self,
                success    =can_check,
                character  =context.character,
                target     =None,
                tool       =None
            ),
            moves=1,
            turns=0,
            score=0
        )

class DefaultAction(Action[tuple]):

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,Description]:
        return True, inputs, None

    def take_action(self, current_state:World, context:ActionContext, inputs:tuple[Target]) -> Feedback:
        response = list[Description]()
        success = False
        if len(inputs) == 0:
            success, r = current_state.can_act(context.character, self)
            response.append(r)
        for target in inputs:
            can_take_act, target_response = current_state.can_act_on(context.character, target, self)
            response.append(target_response)
            if can_take_act:
                success = True
                response.append(target.perform_action_as_target(self))
        if success:
            response.append(context.character.perform_action_as_actor(self))
        response = backup_description([combine_descriptions(response), plain_text_description("Success." if success else "Fail.")])
        return Feedback(
            description=combine_descriptions(response),
            context=DescriptionContext(
                placements =current_state.item_locations,
                action     =self,
                success    =success,
                character  =context.character,
                target     =None if inputs is None else list(inputs),
                tool       =None
            ),
            moves=1,
            turns=int(success),
            score=0
        )
