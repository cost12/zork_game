from dataclasses                import dataclass

from models.state               import State
from models.actors              import TwoWayPath, Path, MultiPath, PathInfo, Target, NamedContainer
from utils.relator              import NameFinder
from readin.description_helpers import DescriptionStrategy, DescriptionContext, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import ItemPlacementContext, ItemPlacementRestriction, Restriction, ItemStateRestriction, ItemStateContext, RestrictionContext, CharacterAchievementContext, CharacterAchievementRestriciton

@dataclass
class DownContext:
    trapdoor : Target
    opened   : State
    open_text : str = "At your feet the trapdoor is still open."
    closed_text : str = "At your feet lies a trapdoor flush with the floor."

class DownDescription(DescriptionStrategy[DownContext]):
    def describe(self, described:NamedContainer, context:DescriptionContext, specific:DownContext) -> str:
        if specific.opened in specific.trapdoor.get_current_state():
            return specific.open_text
        else:
            return specific.closed_text

class FstringDescription(DescriptionStrategy[Target]):
    def describe(self, described: NamedContainer, context:DescriptionContext, specific:Target) -> str:
        r_context = RestrictionContext(context.character, context.placements)
        return f"Above your head is {specific.describe(r_context)} in the ceiling."

def add_to_name_space(name_space:NameFinder):
    paths = [
        TwoWayPath(
            name="Armory West Exit",
            description_context=PlainTextContext("A harsh looking metal doorway leads west."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('armory', 'location'),
                end=name_space.get_from_id("Beehive Room", "location"),
                direction=name_space.get_from_id('west',  'direction')
            ),
            reverse_direction=name_space.get_from_id('northeast', 'direction'),
            reverse_description_context=PlainTextContext("A thick metal door leads northeast."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Attic Down Exit",
            description_context=DownContext(name_space.get_from_id("trapdoor", "target"), name_space.get_from_id("opened", "state")),
            description_strategy=DownDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('attic', 'location'),
                end=name_space.get_from_id("Bedroom", "location"),
                direction=name_space.get_from_id('down',  'direction'),
                passing_restrictions={
                    Restriction[ItemStateContext](ItemStateContext(name_space.get_from_id("trapdoor", "target"), name_space.get_from_id("opened", "state"), "The trapdoor is closed."), ItemStateRestriction())
                },
            ),
            reverse_direction=name_space.get_from_id('up', 'direction'),
            reverse_description_context=DownContext(name_space.get_from_id("trapdoor", "target"), name_space.get_from_id("opened", "state"), "Above your head the trapdoor hangs open.", "Above your head a trapdoor sits flush with the ceiling."),
            reverse_description_strategy=DownDescription(),
            #children=[name_space.get_from_id("trapdoor", "target")], TODO
        ),
        TwoWayPath(
            name="Barn East Exit",
            description_context=PlainTextContext("A large barn door leads east"),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                direction=name_space.get_from_id('east',  'direction'),
                start=name_space.get_from_id('barn', 'location'),
                end=name_space.get_from_id("Beehive Room", "location"),
            ),
            reverse_direction=name_space.get_from_id('northwest', 'direction'),
            reverse_description_context=PlainTextContext("A rustic door lies to the northwest."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        Path(
            name="Bathroom West Exit",
            description_context=PlainTextContext("A thin door leads west, offering no privacy"),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('bathroom', 'location'),
                end=name_space.get_from_id("Beehive Room", "location"),
                direction=name_space.get_from_id('west',  'direction'),
            ),
        ),
        TwoWayPath(
            name="Bear's Den North Exit",
            description_context=PlainTextContext("A narrow escape leads north."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('bears den', 'location'),
                end=name_space.get_from_id("Cold Room", "location"),
                direction=name_space.get_from_id('north',  'direction')
            ),
            reverse_direction=name_space.get_from_id('south',  'direction'),
            reverse_description_context=PlainTextContext("An earthen passage leads south."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Bear's Den South Exit",
            description_context=PlainTextContext("A passage leads south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('bears den', 'location'),
                end=name_space.get_from_id("puzzle room", "location"),
                direction=name_space.get_from_id('south',  'direction')
            ),
            reverse_direction=name_space.get_from_id('north',  'direction'),
            reverse_description_context=PlainTextContext("A stony passage leads north."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        Path(
            name="Bedroom East Exit",
            description_context=PlainTextContext("To the east, you see a doorway."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('bedroom', 'location'),
                end=name_space.get_from_id("Bathroom", "location"),
                direction=name_space.get_from_id('east', 'direction'),
            ),
        ),
        TwoWayPath(
            name="Bedroom South Exit",
            description_context=PlainTextContext("A passage stretches south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('bedroom', 'location'),
                end=name_space.get_from_id("Hallway", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("To the north, you see a doorway."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Beehive Room North Exit",
            description_context=PlainTextContext("A passage goes north."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('beehive room', 'location'),
                end=name_space.get_from_id("Small Cavern", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('south', 'direction'),
            reverse_description_context=PlainTextContext("Amidst dripping stalagmites, a sturdy wooden door is installed to the south."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Beehive Room Southeast Exit",
            description_context=PlainTextContext("A small door goes southeast."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('beehive room', 'location'),
                end=name_space.get_from_id("Skate Park", "location"),
                direction=name_space.get_from_id('southeast', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('northwest', 'direction'),
            reverse_description_context=PlainTextContext("An exit leads northwest."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Beehive Room Southwest Exit",
            description_context=PlainTextContext("A large rocky passage leads southwest."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('beehive room', 'location'),
                end=name_space.get_from_id("Giant Cave", "location"),
                direction=name_space.get_from_id('southwest', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('northeast', 'direction'),
            reverse_description_context=PlainTextContext("A passage leads northeast."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Beehive Room South Exit",
            description_context=PlainTextContext("A scarred wooden door lies to the south"),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('beehive room', 'location'),
                end=name_space.get_from_id("Orge Lair", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("A door leads north."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Bright Room Northeast Exit",
            description_context=PlainTextContext("A passage exists, but you cannot tell in which direction, for you are nearly blinded by the light."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('bright room', 'location'),
                end=name_space.get_from_id("Orge Lair", "location"),
                direction=name_space.get_from_id('northeast', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('southwest', 'direction'),
            reverse_description_context=PlainTextContext("A passage leads south, glowing slightly."),
            reverse_description_strategy=PlainTextDescription(),
            reverse_passing_restrictions={
                Restriction[ItemStateContext](ItemStateContext(name_space.get_from_id("orge", "actor"), name_space.get_from_id("guarding", "state"), "In the middle stands a hulking orge holding a large club, blocking the way to a passage going South."), ItemStateRestriction())
            },
        ),
        Path(
            name="Bright Room Southwest Exit",
            description_context=PlainTextContext("Somewhere in your field of vision is a passage, but you are disoriented by the brightness and cannot tell in which direction it lies."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('bright room', 'location'),
                end=name_space.get_from_id("Theatre Entrance", "location"),
                direction=name_space.get_from_id('southwest', 'direction'),
            ),
        ),
        TwoWayPath(
            name="Candlelit Room East Exit",
            description_context=PlainTextContext("A thin passage slithers eastward."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('candlelit room', 'location'),
                end=name_space.get_from_id("Giant Cave", "location"),
                direction=name_space.get_from_id('east', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('south', 'direction'),
            reverse_description_context=PlainTextContext("A distant hole in the stone room leads south."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Candlelit Room South Exit",
            description_context=PlainTextContext("A grand, ornate doorway leads south, bejewled and intricately chiseled with themes of old."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('candlelit room', 'location'),
                end=name_space.get_from_id("Riches Room", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("A passage leads north."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Car Trunk Exit",
            description_context=PlainTextContext("The garage is outside."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('car trunk', 'location'),
                end=name_space.get_from_id("Parking Lot", "location"),
                direction=name_space.get_from_id('any', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('in trunk', 'direction'),
            reverse_description_context=PlainTextContext(None),
		    reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Cargo Hold North Exit",
            description_context=PlainTextContext("Northwards, the train continues."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('cargo hold', 'location'),
                end=name_space.get_from_id("Conductor's Car", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('south', 'direction'),
            reverse_description_context=PlainTextContext("The train continues southwards."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        Path(
            name="Cargo Hold South Exit",
            description_context=PlainTextContext("Another train car is to the south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id('cargo hold', 'location'),
                end=name_space.get_from_id("Hallway", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
        ),
        Path(
            name="Carpeted Hall East Exit",
            description_context=PlainTextContext("A wooden door awaits you in the east."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("Carpeted Hall", "location"),
                end=name_space.get_from_id("Carpeted Hall", "location"),
                direction=name_space.get_from_id('east', 'direction'),
            ),
        ),
        Path(
            name="Carpeted Hall West Exit",
            description_context=PlainTextContext("In the west, a wooden door stands stoically."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("Carpeted Hall", "location"),
                end=name_space.get_from_id("Theatre Stage", "location"),
                direction=name_space.get_from_id('west', 'direction'),
            ),
        ),
        TwoWayPath(
            name="Cellar East Exit",
            description_context=PlainTextContext("A stone staircase leads east."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("cellar", "location"),
                end=name_space.get_from_id("garden", "location"),
                direction=name_space.get_from_id('east', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('west', 'direction'),
            reverse_description_context=PlainTextContext("A stone stiarcase descends in the west."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        MultiPath(
            name="Chimney Exit",
            description_context=PlainTextContext("The fireplace opening is at your feet."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("chimney", "location"),
                end=name_space.get_from_id("attic", "location"),
                direction=name_space.get_from_id('any', 'direction'),
            ),
            multi_end={
                name_space.get_from_id("slide whistle", "target") : name_space.get_from_id("theatre stage", "location")
            }
        ),
        TwoWayPath(
            name="Coach Car North Exit",
            description_context=PlainTextContext("The train continues to the north."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("coach car", "location"),
                end=name_space.get_from_id("Dining Car", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('south', 'direction'),
            reverse_description_context=PlainTextContext("The train continues south."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        Path(
            name="Coach Car South Exit",
            description_context=PlainTextContext("A sliding door leads south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("coach car", "location"),
                end=name_space.get_from_id("Museum Gallery", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
        ),
        TwoWayPath(
            name="Cold Room North Exit",
            description_context=PlainTextContext("A small passage leads north."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("cold room", "location"),
                end=name_space.get_from_id("south of tight pass", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('south', 'direction'),
            reverse_description_context=PlainTextContext("A frigid draft is coming from a passage leading south."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Conductor's Car North Exit",
            description_context=PlainTextContext("The train's exit is to the North."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("conductor's car", "location"),
                end=name_space.get_from_id("Hot Room", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('south', 'direction'),
            reverse_description_context=PlainTextContext("A passage leads south, eminating some contionuous noise."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Crystal Cave West Exit",
            description_context=PlainTextContext("A passage leads west"),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("crystal cave", "location"),
                end=name_space.get_from_id("Greenhouse", "location"),
                direction=name_space.get_from_id('west', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('east', 'direction'),
            reverse_description_context=PlainTextContext("A passage leads east."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Crystal Cave South Exit",
            description_context=PlainTextContext("A passage leads south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("crystal cave", "location"),
                end=name_space.get_from_id("Pool", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("A cool passage leads north, emitting a cool breeze."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Den North Exit",
            description_context=PlainTextContext("To the north is a doorway."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("den", "location"),
                end=name_space.get_from_id("hallway", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('south', 'direction'),
            reverse_description_context=PlainTextContext("Southwards lies a doorway."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Den South Exit",
            description_context=PlainTextContext("A passageway leads south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("den", "location"),
                end=name_space.get_from_id("garden", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("The house's tattered front door lies to the north, slightly ajar."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Den East Exit",
            description_context=PlainTextContext("A doorway leads east."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("den", "location"),
                end=name_space.get_from_id("kitchen", "location"),
                direction=name_space.get_from_id('east', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('west', 'direction'),
            reverse_description_context=PlainTextContext("To the west is a doorway."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Den West Exit",
            description_context=PlainTextContext("A closed swinging door lies to the west."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("den", "location"),
                end=name_space.get_from_id("dining room", "location"),
                direction=name_space.get_from_id('west', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('east', 'direction'),
            reverse_description_context=PlainTextContext("A door goes east."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Dining Car North Exit",
            description_context=PlainTextContext("You are standing in a train's dining car. A thin counter and spaced stools line the East wall, though no places are set. The train rocks gently, riding Northwards, trees whizzing past as you pass through a dense deciduous forest. A tinkling bouquet of music frolics around the car."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("dining car", "location"),
                end=name_space.get_from_id("Observation car", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('south', 'direction'),
            reverse_description_context=PlainTextContext("The train continues south."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Dining Room North Exit",
            description_context=PlainTextContext("A doorway leads north."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("dining room", "location"),
                end=name_space.get_from_id("office", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('south', 'direction'),
            reverse_description_context=PlainTextContext("A doorway leads southward."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Display Room West Exit",
            description_context=PlainTextContext("A simple slanted passage leads west."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("display room", "location"),
                end=name_space.get_from_id("man cave", "location"),
                direction=name_space.get_from_id('west', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('east', 'direction'),
            reverse_description_context=PlainTextContext("An ornate doorway leads to the east."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Driver's Seat Out Exit",
            description_context=PlainTextContext("The door leads out."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("driver's seat", "location"),
                end=name_space.get_from_id("parking lot", "location"),
                direction=name_space.get_from_id('out', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('in car', 'direction'),
            reverse_description_context=PlainTextContext("The driver's door."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Earthen Tunnel North Exit",
            description_context=PlainTextContext("A passage slopes northwards."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("earthen tunnel", "location"),
                end=name_space.get_from_id("Garden", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('south', 'direction'),
            reverse_description_context=PlainTextContext("A narrow earthen burrow leads south."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Earthen Tunnel South Exit",
            description_context=PlainTextContext("A passage leads south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("earthen tunnel", "location"),
                end=name_space.get_from_id("small cavern", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("A narrow tunnel leads to the north."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        Path(
            name="Greenhouse North Exit",
            description_context=PlainTextContext("A passage leads north."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("greenhouse", "location"),
                end=name_space.get_from_id("beehive room", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
        ),
        MultiPath(
            name="Gym North Exit",
            description_context=PlainTextContext("A metal doorway leads north."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("gym", "location"),
                end=name_space.get_from_id("pool", "location"),
                direction=name_space.get_from_id('north', 'direction'),
                passing_restrictions=[
                    Restriction[CharacterAchievementContext](CharacterAchievementContext(name_space.get_from_id("score", "achievement"), "You can't seem to exit."), CharacterAchievementRestriciton())
                ],
            ),
            multi_end={
                name_space.get_from_id("bongo", "target") : name_space.get_from_id("Theatre stage", "location")
            },
        ),
        TwoWayPath(
            name="Hallway East Exit",
            description_context=PlainTextContext("To the east is a doorway."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("hallway", "location"),
                end=name_space.get_from_id("kitchen", "location"),
                direction=name_space.get_from_id('east', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("To the north is a doorway."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        Path(
            name="Hot Room Northeast Exit",
            description_context=PlainTextContext("A passage leads northeast."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("hot room", "location"),
                end=name_space.get_from_id("theatre stage", "location"),
                direction=name_space.get_from_id('northeast', 'direction'),
            ),
        ),
        MultiPath(
            name="Library North Exit",
            description_context=PlainTextContext("A regal yet sturdy double door leads north."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("library", "location"),
                end=name_space.get_from_id("puzzle room", "location"),
                direction=name_space.get_from_id('north', 'direction'),
                passing_restrictions=[
                    Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("red book", "target"), name_space.get_from_id("shelf 3 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
                    Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("gray book", "target"), name_space.get_from_id("shelf 4 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
                    Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("brown book", "target"), name_space.get_from_id("shelf 5 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
                    Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("yellow book", "target"), name_space.get_from_id("shelf 6 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
                    Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("emerald book", "target"), name_space.get_from_id("shelf 7 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
                    Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("burgundy book", "target"), name_space.get_from_id("shelf 8 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction()),
                    Restriction[ItemPlacementContext](ItemPlacementContext(name_space.get_from_id("vermilion book", "target"), name_space.get_from_id("shelf 9 library", "locationdetail"), "You can't exit."), ItemPlacementRestriction())
                ],
            ),
            multi_end={
                name_space.get_from_id("violin", "target") : name_space.get_from_id("theatre stage", "location")
            },
        ),
        Path(
            name="Man Cave Northwest Exit",
            description_context=PlainTextContext("A passage leads northwest."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("man cave", "location"),
                end=name_space.get_from_id("theatre stage", "location"),
                direction=name_space.get_from_id('northwest', 'direction'),
            ),
        ),
        TwoWayPath(
            name="Man Cave South Exit",
            description_context=PlainTextContext("A passage leads south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("man cave", "location"),
                end=name_space.get_from_id("north of tight pass", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("A passage leads to the north, emitting an unpleasant odor."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        MultiPath(
            name="Museum north Exit",
            description_context=PlainTextContext("A curtained passage proceeds northwards."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("museum", "location"),
                end=name_space.get_from_id("coach car", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            multi_end={
                name_space.get_from_id("lyre", "target") : name_space.get_from_id("Theatre stage", "location")
            }
        ),
        TwoWayPath(
            name="North of Tight Pass South Exit",
            description_context=PlainTextContext("The tight pass continues south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("north of tight pass", "location"),
                end=name_space.get_from_id("south of tight pass", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("The tight pass leads north."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        Path(
            name="Observation Car North Exit",
            description_context=PlainTextContext("The train continues north."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("observation car", "location"),
                end=name_space.get_from_id("cargo hold", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
        ),
        MultiPath(
            name="Parking Lot North Exit",
            description_context=PlainTextContext("An exit ramp leads to the north."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("parking lot", "location"),
                end=name_space.get_from_id("riches room", "location"),
                direction=name_space.get_from_id('north', 'direction'),
            ),
            multi_end={
                name_space.get_from_id("triangle", "target") : name_space.get_from_id("theatre stage", "location")
            }
        ),
        Path(
            name="Pool South Exit",
            description_context=PlainTextContext("A passage leads south, smelling of body odor."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("pool", "location"),
                end=name_space.get_from_id("gym", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
        ),
        Path(
            name="Puzzle Room South Exit",
            description_context=PlainTextContext("A nice walkway leads south"),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("puzzle room", "location"),
                end=name_space.get_from_id("library", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
        ),
        Path(
            name="Riches Room South Exit",
            description_context=PlainTextContext("A cement walkway goes to the south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("riches room", "location"),
                end=name_space.get_from_id("parking lot", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
        ),
        Path(
            name="Skate Park South Exit",
            description_context=PlainTextContext(None),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("skate park", "location"),
                end=name_space.get_from_id("greenhouse", "location"),
                direction=name_space.get_from_id('south', 'direction'),
                hidden_when_locked=True,
                passing_restrictions=[
                    Restriction[CharacterAchievementContext](CharacterAchievementContext(name_space.get_from_id("gift skateboard to child", "achievement"), "A mysterious force prevents you from exiting."), CharacterAchievementRestriciton())
                ]
            ),
        ),
        MultiPath(
            name="Theatre Entrance North Exit",
            description_context=PlainTextContext("A gilded double door leads north, slight light streaking through the thin gap running down their seam."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("theatre entrance", "location"),
                end=None,
                direction=name_space.get_from_id('north', 'direction'),
            ),
            multi_end={
                name_space.get_from_id("baton",         "target") : name_space.get_from_id("bright room",    "location"),
                name_space.get_from_id("lyre",          "target") : name_space.get_from_id("museum gallery", "location"),
                name_space.get_from_id("triangle",      "target") : name_space.get_from_id("parking lot",    "location"),
                name_space.get_from_id("slide whistle", "target") : name_space.get_from_id("chimney",        "location"),
                name_space.get_from_id("bongo",         "target") : name_space.get_from_id("gym",            "location"),
                name_space.get_from_id("violin",        "target") : name_space.get_from_id("library",        "location")
            }
        ),
        TwoWayPath(
            name="Theatre Entrance South Exit",
            description_context=PlainTextContext("The Theatre's seating area lies in the south."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("theatre entrance", "location"),
                end=name_space.get_from_id("theatre seats", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("The Theatre's entryway lies in the north."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        TwoWayPath(
            name="Theatre Seats South Exit",
            description_context=PlainTextContext("The Theatre's stage is southwards."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("theatre seats", "location"),
                end=name_space.get_from_id("Theatre Stage", "location"),
                direction=name_space.get_from_id('south', 'direction'),
            ),
            reverse_direction=name_space.get_from_id('north', 'direction'),
            reverse_description_context=PlainTextContext("The Theatre continues to the north, full of seats."),
            reverse_description_strategy=PlainTextDescription(),
        ),
        MultiPath(
            name="Theatre Stage Southeast Exit",
            description_context=PlainTextContext("A passage embellished with arcane runes leads southeast."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("theatre stage", "location"),
                end=None,
                direction=name_space.get_from_id('southeast', 'direction'),
            ),
            multi_end={
                name_space.get_from_id("baton",         "target") : name_space.get_from_id("carpeted hall",  "location"),
                name_space.get_from_id("lyre",          "target") : name_space.get_from_id("museum gallery", "location"),
                name_space.get_from_id("triangle",      "target") : name_space.get_from_id("parking lot",    "location"),
                name_space.get_from_id("slide whistle", "target") : name_space.get_from_id("chimney",        "location"),
                name_space.get_from_id("bongo",         "target") : name_space.get_from_id("gym",            "location"),
                name_space.get_from_id("violin",        "target") : name_space.get_from_id("library",        "location")
            }
        ),
        MultiPath(
            name="Theatre Stage Southwest Exit",
            description_context=PlainTextContext("A passage garnished with ancient symbology leads southwest."),
            description_strategy=PlainTextDescription(),
            path_info=PathInfo(
                start=name_space.get_from_id("theatre stage", "location"),
                end=None,
                direction=name_space.get_from_id('southwest', 'direction'),
            ),
            multi_end={
                name_space.get_from_id("baton",         "target") : name_space.get_from_id("hot room",       "location"),
                name_space.get_from_id("lyre",          "target") : name_space.get_from_id("museum gallery", "location"),
                name_space.get_from_id("triangle",      "target") : name_space.get_from_id("parking lot",    "location"),
                name_space.get_from_id("slide whistle", "target") : name_space.get_from_id("chimney",        "location"),
                name_space.get_from_id("bongo",         "target") : name_space.get_from_id("gym",            "location"),
                name_space.get_from_id("violin",        "target") : name_space.get_from_id("library",        "location")
            }
        ),
    ]

    name_space.add_many(paths)
