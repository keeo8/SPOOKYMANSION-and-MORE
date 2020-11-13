import json

# This global dictionary stores the name of the room as the key and the dictionary describing the room as the value.
GAME = {
    '__metadata__': {
        'title': 'Adventure',
        'start': 'classroom'
    }
}

def create_room(name, description, ends_game=False):
    """
    Create a dictionary that represents a room in our game.

    INPUTS:
     name: string used to identify the room; think of this as a variable name.
     description: string used to describe the room to the user.
     ends_game: boolean, True if arriving in this room ends the game.
    
    RETURNS:
     the dictionary describing the room; also adds it to GAME!
    """
    assert (name not in GAME)
    room = {
        'name': name,
        'description': description,
        'exits': [],
        'items': [],
    }
    # Does this end the game?
    if ends_game:
        room['ends_game'] = ends_game

    # Stick it into our big dictionary of all the rooms.
    GAME[name] = room
    return room

def create_exit(source, destination, description):
    """
    Rooms are useless if you can't get to them! This function connects source to destination (in one direction only.)

    INPUTS:
     source: which room to put this exit into (or its name)
     destination: where this exit goes (or its name)
     description: how to show this exit to the user (ex: "There is a red door.")
     required_key (optional): string of an item that is needed to open/reveal this door.
     hidden (optional): set this to True if you want this exit to be hidden initially; until the user types 'search' in the source room.
    """
    # Make sure source is our room!
    if isinstance(source, str):
        source = GAME[source]
    # Make sure destination is a room-name!
    if isinstance(destination, dict):
        destination = destination['name']
    # Create the "exit":
    exit = {
        'destination': destination,
        'description': description
    }
    source['exits'].append(exit)
    return exit

##
# Let's imagine 4 places:
# Note that earlier, in __metadata__ we said that we should start in classroom.
##
classroom = create_room("classroom", "You're in a lecture hall, for some reason.")
hallway = create_room("hallway", "This is a hallway with many locked doors.")
staircase = create_room("staircase", "The staircase leads downward.")
outside = create_room("outside", "You've escaped! It's cold out.", ends_game=True)
classroom2= create_room("new classroom", "You step in and see Laurie Patton teaching a lecture! What a great president! Also, everyone is looking at you.")
desk = create_room("desk", "The moment you sit down, you fall into a zen-like trance. Laurie Patton serenades you with the history of religious history. After 75 minutes, you gain an honorary degree and graduate mega clam chowder", ends_game=True)
##
# Let's connect them together.
# It's not a very fun adventure, but it's simple.
##
create_exit(classroom, hallway, "A door leads into the hall.")
# If you want doors to work in both directions; you have to do that yourself.
create_exit(hallway, classroom, "Go back into the classroom.")
create_exit(hallway, classroom2, "You see a slightly opened mahogany door letting chatter echo into the hallway, of course you want to open it!")

create_exit(classroom2, hallway, "You run out of the room, tears streaming down your face. How could you embarass yourself that badly?")
create_exit(classroom2, desk, "Well so what if people stare, you came here to learn and thus take a seat in an open desk. Noone is sitting there due to covid restriction. However, you already counted how many beds there were and, with the n+2 rule, you seemed safe to sit down.")
# Note we can also refer to places by their names (same as their variables for my sanity!)
create_exit('hallway', 'staircase', "A door with the words STAIRS is stuck open.")
create_exit(staircase, hallway, "Nevermind; go back to the hallway.")

create_exit(staircase, outside, "A door at the bottom of the stairs has a red, glowing, EXIT sign.")
# we don't go back from outside, because the game ends as soon as we get there.

##
# Save our text-adventure to a file:
##
with open('adventure.json', 'w') as out:
    json.dump(GAME, out, indent=2)
