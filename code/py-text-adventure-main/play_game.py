import json, os, time
import random

def main():
    # TODO: allow them to choose from multiple JSON files?
    with open(picker()) as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)
    
def picker():
    for n, i in enumerate(os.listdir()):
        print(n, i)
    answer = int(input('Which game do you want to play?'))
    file = os.listdir()[answer]
    return str(file)



def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    initial = time.time()

    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        
        #what time is it?
        current = time.time()
        spent = current - initial
        spent = spent / 60
        print("You have been in the mansion for " + str(round(spent, 2)) + " minutes")
        
        
        
        # Print the description.
        print(here["description"])
        
        #smells like a cat
        
        chance = random.randint(0,100)
        if chance < 30:
            print("You also notice a little black cat looking back at you from the floor.")    
        
        # TODO: print any available items in the room...
        itemlist = here['items']
        if len(itemlist) > 0:
            print('There is a', itemlist)
        
        # e.g., There is a Mansion Key.
        
        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        
        if action in ["help"]:
            print_instructions()
            continue
        
        if action in ["stuff"]:
            if len(stuff) >0:
                print(stuff)
            else: 
                print('You have nothing')
            continue
        
        if action in ["take"]:
            stuff.extend(here['items']) #note to self: some things are better than append
            here['items'].clear()
            print("You picked up ")
            continue
        
        if action in ['drop']:
            for n, i in enumerate(stuff):
                print(n, i)
        
            choice = int(input("Which item do you want to drop?"))
            k = stuff.pop(choice)
            here['items'].append(k)
            print("You dropped " + k)
            
            if chance < 30:
                if k == 'Kitty Treat':
                    print('The little black cat quickly dashes to pick up the snack and starts to purr')
            continue
        
        if action in ["search"]:
            for exit in here['exits']:
                if "hidden" in exit:
                    exit['hidden'] = False
                    print("You found something")
            
            continue
        
                    
            

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if "required_key" in selected:
                if selected['required_key'] in stuff:
                    current_place = selected['destination']
                    print("...")
                else:
                    print("OOF, looks like you might need a key for that door")
            else:
                current_place = selected['destination']
                print("...")
        except :
            print("I don't understand '{}'...".format(action))
       
        
        
        
    print("")
    print("")
    print("=== GAME OVER ===")

def find_usable_exits(room):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable 


def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'help' to reload instructions.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()
