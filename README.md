# Thief

Thief is a Zork style game where users control their player through the command line and attempt to solve puzzles and reach their destination.

## Creating a Level

Levels are built by reading in jsons from the data folder. A level will have achievements, actions, characters, controllers for the characters, directions, items, rooms, skills, skill sets, states, state graphs, and other miscellaneous details.

### Common Variables

#### aliases

Alternative names for an object. The primary name will be added to this list if it is not included. Users can reference an object using any of it's aliases (case insensitive). Multiple objects can share the same alias. The interpreter may ask questions to disambiguate any references to shared aliases.

#### description

A description can be defined for any visible object. 

#### id

A unique identifier for an object. Each id must be unique (case insensitive). If no id is given, id defaults to name for most objects. Path ids default to 'f"{name} going {direction_name} in {room_name}"' where name is the path name, direction_name is the name of the direction the path leads, and room_name is the name of the room the path starts. LocationDetail ids default to 'f"{name} {parent_id}"' where name is the LocationDetail name and parent_id is the id of the id of the object that contains the location detail. If the default id for an object would not be unique, it needs to be defined. Ids are not used to reference an object in the game unless it is needed for disambiguation.

#### name

The primary name of an object. The game will always refer to an object by it's primary name (keeping capitalization) when printing out. Mulitple objects can share the same name.


### Responses

#### Backup

Currently not an option. Has a list of responses and return the first one that doesn't evaluate to None.

#### Combination

Joins a list of responses by a join string. The default join string is the empty string. Currently the join string can't be changed.

To use a combination response make a list of responses where a single response would usually go.

Example:
'
{
    "description" : ["Response 1", "response 2", ["nested response"], ...]
}
'

#### Contents

#### Contents With State

#### Item State

#### Random

#### Static

### Achievements

Achievements represent notable actions that a character completes. This could include visiting a certain number of rooms. Achievements can be meaningless but they can also be required to complete certain actions. For example, making a shot to leave a room.

To create an achievement you need to define a name. ex:
'
{
    "name"    : "AchievementName",
    "id"      : "AchievementId",
    "aliases" : ["Alias1", ..., "AliasN"]
}
'
Defining an id and aliases are optional.

### Actions

Actions represent all the moves a character can take on their turn. This includes moving between rooms and interacting with items/other characters. Actions also require a function to define their interactions with objects. 

To create an action you need to define a name. ex:
'
{
    "name"    : "ActionName",
    "id"      : "ActionId",
    "aliases" : ["Alias1", ..., "AliasN"]
}
'
Defining an id and aliases are optional.

### Characters

Characters represent user controlled or computer controlled agents. 

To create a character you need to define a name, type, description, state, skills, and inventory.