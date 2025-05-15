# Thief

Thief is a Zork style game where users control their player through the command line and attempt to solve puzzles and reach their destination.

## Creating a Level

Levels are built by reading in jsons from the data folder. A level will have achievements, actions, characters, controllers for the characters, directions, items, rooms, skills, skill sets, states, state graphs, and other miscellaneous details.

## Common Variables

### aliases

Alternative names for an object. The primary name will be added to this list if it is not included. Users can reference an object using any of it's aliases (case insensitive). Multiple objects can share the same alias. The interpreter may ask questions to disambiguate any references to shared aliases.

### description

A description can be defined for any visible object. 

### id

A unique identifier for an object. Each id must be unique (case insensitive). If no id is given, id defaults to name for most objects. Path ids default to `f"{name} going {direction_name} in {room_name}"` where name is the path name, direction_name is the name of the direction the path leads, and room_name is the name of the room the path starts. LocationDetail ids default to `f"{name} {parent_id}"` where name is the LocationDetail name and parent_id is the id of the id of the object that contains the location detail. If the default id for an object would not be unique, it needs to be defined. Ids are not used to reference an object in the game unless it is needed for disambiguation.

**When creating the game/in the jsons everything is referred to by its id.**

### name

The primary name of an object. The game will always refer to an object by it's primary name (keeping capitalization) when printing out. Mulitple objects can share the same name.


## Responses

Responses control how the game conveys information/text to the user. They can be triggered by looking at an object (description), performing an action on/with an objects (target/actor/tool responses), or when an object enters a new state (state responses). Responses allow for nesting of other response types inside them.

For each of the response types, the object they refer to is assumed to be their parent. You can specify `"target": "target_id"` (where target_id is the id of the object that the response will depend on) in the response dict to specify that the response depends on another item. For example, a description of table could depend on the objects resting on the table or you might decide (for some reason) that the table should appear different depending on placement of a book in another room. Then you would have to specify the `"target": "book_id"` (or whatever the book's id might be) for the table's description.

### Backup

Currently not an option. Has a list of responses and return the first one that doesn't evaluate to None.

### Combination

Joins a list of responses by a join string. The default join string is the empty string. Currently the join string can't be changed.

To use a combination response make a list of responses where a single response would usually go.

Example:

{

    "description" : ["Response 1", "response 2", ["nested response", ...], {...}, ...]

}

### Contents

Lists the contents of an item/character/detail. Also takes alternative text for the case where the object is empty.

To use a contents response specify full and empty responses and the type of response (contents):

{

    "description" : {

        "type" : "contents",

        "full" : "The contents of this object are",

        "empty": "This object has no contents"

    }

}

### Contents With State

Checks the contents of an object to see if any of the contents have a specific state then returns a response accordingly. If the contents of the object have mutiple states, the responses will be returned in a random order separated by a space. A response for a single state can be returned at most once.

To use a contents with state response spcecify the responses for each state, an optional default, and the type of response (contents_with_state):

{

    "description" : {

        "type" : "contents_with_state",

        "responses" : {

            "state1" : "Object has at least one item with state1."

            "state2" : "Object has at least one item with state2."

            ...

        }

        "default" : "Object has no items with any of the states."

    }

}

### Item State

Gives a different response depending on the current state of an object. If the object has mutiple listed states, the responses will be returned in a random order separated by a space.

To use an item state response specify the responses for each state, an optional default, and the type of response (item_state):

{

    "description" : {

        "type" : "item_state",

        "responses" : {

            "state1" : "Object has state state1.",
            
            "state2" : "Object has state state2.",

            ...

        }

        "default" : "Object has none of the states."

    }

}

### Random

Returns one response from a list of responses, each with equal probability.

To use a random response specify a list of responses and the type of response (random):

{

    "description" : {

        "type" : "random",

        "responses" : ["Option 1", "Option 2", ["nested option", ...], {...}, ...]

    }

}

### Static

The simplest type of response. Returns the same string every time.

To use a static response just give the string to return:

{

    "description": "Simple description"

}

## Achievements

Achievements represent notable actions that a character completes. This could include visiting a certain number of rooms. Achievements can be meaningless but they can also be required to complete certain actions. For example, making a shot to leave a room.

To create an achievement you need to define a name. ex:

{

    "name"    : "AchievementName",

    "id"      : "AchievementId",

    "aliases" : ["Alias1", ..., "AliasN"]

}

Defining an id and aliases are optional.

## Actions

Actions represent all the moves a character can take on their turn. This includes moving between rooms and interacting with items/other characters. Actions also require a function to define their interactions with objects. 

To create an action you need to define a name. ex:

{

    "name"    : "ActionName",

    "id"      : "ActionId",

    "aliases" : ["Alias1", ..., "AliasN"]

}

Defining an id and aliases are optional.

## Characters

Characters represent user controlled or computer controlled agents. 

To create a character you need to define a name, type, description, state, skills, and inventory.