import time
import keyboard
import os
import copy
from enum import Enum
import hashlib
# from sys import exit

# constants
INVENTORY = "inventory"
WALL = "#"
HOE  = "h"
BLANK = " "
PLAYER = "@"
SHIP = "S"
SEED = "."
SEEDLING = ","
SPROUT = "i"
POTATO = "p"
TILLED_SOIL = "t"
ITEMS = [HOE, POTATO]
STACKABLE = [SEED, POTATO]

WORD_ITEM = {
    SEED : "seed",
    HOE  : "hoe",
    SEEDLING : "seedling",
    SPROUT : "sprout",
    POTATO : "potato",
    TILLED_SOIL : "tilled soil"
}

# Stats
POTATO_GAINS = 5
MAX_HEALTH = 100
MAX_SATIATION = 100
HUNGER_INTERVAL = 20


# Mesasges
SHIP_OUT_OF_SEEDS = "Ship currently has 0 seeds. Try again later."
MESSAGE_TIME_LIMIT = 10
MAX_MESSAGES = 10

# globals
clock_start = 0
clock = 0
world = []
item_map = {} # { (x, y) : 'item' }
player = {
    "pos" : (),
    "inventory" : {},
    "equipped" : None,
    "health" : MAX_HEALTH,
    "hunger" : MAX_SATIATION
}
ship_pos = ()
feedback_messages = []
seed_tracker = [] # [ (x, y, clock) ]
seed_stages = [SEED, SEEDLING, SPROUT, POTATO]
seed_growth_time = 30
last_observed_item = None
prev_state_hash = None
hunger_last_decrement = 0

input_time = 0.0
input_interval = .15

# def is_matching(coord1, coord2):
#     assert len(coord1) == len(coord2) == 2
#     if coord1[0] != coord2[0]:
#         return False
#     if coord1[1] != coord2[1]:
#         return False
#     return True


def parse_tile(x, y, tile, world_row):
    global item_map
    global ship_pos
    if tile == PLAYER:
        player["pos"] = (x, y)
        world_row.append(BLANK)
    elif tile == SHIP:
        ship_pos = (x, y)
        world_row.append(BLANK)
    elif tile in ITEMS:
        item_map[(x, y)] = tile
        world_row.append(BLANK)
    else:                    
        world_row.append(tile)


def load_world(filename):
    global world
    global clock_start

    clock_start = int(time.time())

    with open(filename, 'r', encoding='utf8') as handle:
        for y, line in enumerate(handle):
            line = line.strip()
            world_row = []
            for x, tile in enumerate(line):
                parse_tile(x, y, tile, world_row)                
            world.append(world_row)
    for row in world:
        print(*row, sep='')
    # input("Press enter to continue...")


def poll_user_input():
    global input_time
    
    if time.time() - input_time < input_interval:
        return

    x, y = player["pos"]
    if keyboard.is_pressed('w') and world[y-1][x] != WALL:
        player["pos"] = (x, y-1)
        input_time = time.time()
    if keyboard.is_pressed('a') and world[y][x-1] != WALL:
        player["pos"] = (x-1, y)
        input_time = time.time()
    if keyboard.is_pressed('s') and world[y+1][x] != WALL:
        player["pos"] = (x, y+1)
        input_time = time.time()
    if keyboard.is_pressed('d') and world[y][x+1] != WALL:
        player["pos"] = (x+1, y)
        input_time = time.time()
    if keyboard.is_pressed('space') and player["equipped"]:
        player_action()
        input_time = time.time()
    if keyboard.is_pressed('1'):
        input_time = time.time()
        if is_player_in_ship():
            try_dispense_seeds()
        else:
            try_equip_item(1)
    if keyboard.is_pressed('2'):
        input_time = time.time()
        try_equip_item(2)
    if keyboard.is_pressed('3'):
        input_time = time.time()
        try_equip_item(3)


def player_action():
    global world    
    global seed_tracker

    # Ignore 'spacebar' action if player in ship
    if is_player_in_ship():
        return

    x, y = player["pos"]
    if player["equipped"] == HOE and world[y][x] == BLANK:
        world[y][x] = TILLED_SOIL
        print_feedback("You tilled the earth and made the land fertile.")
    elif player["equipped"] == SEED and world[y][x] == TILLED_SOIL:
        world[y][x] = SEED
        seed_tracker.append( (x, y, clock) )
        print_feedback("You planted the mighty seed in fertile soil.")
        player["inventory"][SEED] -= 1
        if player["inventory"][SEED] < 1:
            del player["inventory"][SEED]
            player["equipped"] = None
    elif player["equipped"] == SEED and world[y][x] == BLANK:
        print_feedback("The soil is not tilled. It would be a shame to waste a seed..")


def is_player_in_ship():
    return ship_pos == player["pos"]


def print_ship_menu():
    print("SHIP MENU: Press [1] to get seeds. Press [2] to get egg.")    


def print_feedback(message):
    global feedback_messages
    feedback_messages.append(( message, clock ))

    num_messages = len(feedback_messages)
    for _ in range(0, num_messages - MAX_MESSAGES, 1):
        feedback_messages.pop(0)



def try_dispense_seeds():
    global feedback_messages
    global player
    if SEED in player["inventory"]:
        print_feedback(SHIP_OUT_OF_SEEDS)        
        return
    player["inventory"][SEED] = 10


def try_equip_item(keypressed):
    global player    
    index = 0
    items = list(player["inventory"].keys())
    if (keypressed) > len(items):
        return
    item = items[keypressed - 1]    
    if item == player["equipped"]:
        return
    if item == POTATO:
        print_feedback("You feasted on the super potato satisfied your hunger")
        player["hunger"] = MAX_SATIATION
    else:
        player["equipped"] = item
        print_feedback("You equipped the mighty " + WORD_ITEM[item])
    index += 1


def print_inventory():
    inventory_output = "Inventory: "
    hotkey = 1
    for item, count in player["inventory"].items():
        item_word = WORD_ITEM[item]
        if count > 1:
            inventory_output += "[" + str(hotkey) + "] " + item_word + " x" + str(count) + "   "
        else:
            inventory_output += "[" + str(hotkey) + "] " + item_word + "   "
        hotkey += 1
    print(inventory_output)
    equipped = None
    if player["equipped"]:
        equipped = WORD_ITEM[player["equipped"]]
    print("Equipped:", equipped)


def print_player_stats():
    health = player["health"]
    hunger = player["hunger"]
    print(f"Health {health} : Hunger {hunger}")


def observe_world():
    global last_observed_item
    
    x, y = player["pos"]
    item = world[y][x]
    if last_observed_item == item:
        return
    if item not in WORD_ITEM:
        return 
    word_item = WORD_ITEM[item]
    if item == TILLED_SOIL:
        print_feedback(f"This looks like {word_item}")
    else:
        print_feedback(f"This looks like a {word_item}")
    last_observed_item = item


def process():
    global player_in_ship
    global clock
    global hunger_last_decrement

    clock = int(time.time()) - clock_start

    observe_world()

    # user input
    poll_user_input()

    # check for items
    if player["pos"] in item_map:        
        position = player["pos"]
        item = item_map[position]
        if item == SHIP:
            pass
        elif item in STACKABLE:
            player["inventory"].setdefault(item, 0)
            player["inventory"][item] += 1
            del item_map[position]
        else:
            player["inventory"][item] = 1
            del item_map[position]

    # Auto-equip item
    if player["equipped"] is None and player["inventory"]:
        try_equip_item(1)

    # grow the seeds
    for i, seed_tuple in enumerate(seed_tracker):
        x, y, seed_clock = seed_tuple
        if clock - seed_clock < seed_growth_time:
            continue        
        index = seed_stages.index(world[y][x])
        index += 1
        if index < len(seed_stages) - 1:            
            world[y][x] = seed_stages[index]
        if index == len(seed_stages) - 1:
            world[y][x] = BLANK
            item_map[(x, y)] = POTATO
            del seed_tracker[i]
        else:
            seed_tracker[i] = (x, y, clock)
                
    # decrement player hunger
    if clock % HUNGER_INTERVAL == 0 and clock != hunger_last_decrement:
        hunger_last_decrement = clock
        player["hunger"] -= 1

    # delete expired messages
    for i, message_tuple in enumerate(feedback_messages):
        message, message_clock = message_tuple
        if clock - message_clock > MESSAGE_TIME_LIMIT:
            del feedback_messages[i]


def render():
    global feedback_messages    
    global prev_state_hash
    
    # Check if render required
    world_state = []
    world_state.append(player)
    world_state.append(world)
    world_state.append(item_map)
    world_state.append(feedback_messages)
    world_hash = hashlib.md5(str(world_state).encode('utf8')).hexdigest()
        
    if prev_state_hash == world_hash:
        return

    prev_state_hash = world_hash

    # Render scene

    os.system('cls')
    world_scene = copy.deepcopy(world)
    
    # add player to scene
    x, y = player["pos"]
    world_scene[y][x] = PLAYER

    # add ship to scene
    x, y = ship_pos
    world_scene[y][x] = SHIP

    # add items to world scene
    for position, item in item_map.items():
        x, y = position
        world_scene[y][x] = item
        
    # render game
    for row in world_scene:
        print(*row, sep='')        
    
    print_player_stats()
    print_inventory()

    if is_player_in_ship():
        print_ship_menu()
    
    # display feedback messages
    for message_tuple in feedback_messages:
        message, _ = message_tuple
        print(message)

    print("state:", prev_state_hash)


if __name__ == "__main__":        
    load_world("world.txt")
    while True:
        process()
        render()
        # time.sleep(0.12)
        
