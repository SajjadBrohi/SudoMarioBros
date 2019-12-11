"""
CSSE1001 2019s2a1
"""

from a1_support import *


def get_position_in_direction(position, direction):
    """Returns the position after moving from given position and direction.

    Parameters:
        position (tuple<int, int>): The row, column position of a tile.
        direction (str): The direction to move.

    Returns:
        (tuple<int, int>): Returns the row, column of the new position.
    """
    if direction == RIGHT:
        position = (position[0]+1, position[1])
    elif direction == LEFT:
        position = (position[0]-1, position[1])
    elif direction == UP:
        position = (position[0], position[1]+1)
    elif direction == DOWN:
        position = (position[0], position[1]-1)
        
    return position

    
def get_tile_at_position(level, position):
    """Returns the tile at the given position in the given level.

    Parameters:
        level (str): The entire string of the level.
        position (tuple<int, int>): The row, column position of a tile.

    Returns:
        (str): The string character of the tile in the given position.
    """
    return level[position_to_index(position,level_size(level))]

    
def get_tile_in_direction(level, position, direction):
    """Returns the tile at the given position, level, and direction.

    Parameters:
        level (str): The entire string of the level.
        position (tuple<int, int>): The row, column position of a tile.
        direction (str): The direction to move.

    Returns:
        (str): The string character of the tile in the given position.
    """
    size = level_size(level)
    new_position = get_position_in_direction(position, direction)
    return level[position_to_index(new_position,size)]


def remove_from_level(level, position):
    """Replaces the tile at the given level & position with the AIR tile.

    Parameters:
        level (str): The entire string of the level.
        position (tuple<int, int>): The row, column position of a tile.

    Returns:
        (str): The level string with the tile replaced
    """
    new_position = position_to_index(position,level_size(level))
    new_level = ''
    
    for i, j in enumerate(level):
        if i == new_position: #Add tile AIR if tile number equals new position
            new_level += AIR
        else: #Otherwise add all the tiles normally
            new_level += j
            
    return new_level


def move(level, position, direction):
    """Updates the position until the updated position isn't a WALL or AIR tile.

    Parameters:
        level (str): The entire string of the level.
        position (tuple<int, int>): The row, column position of a tile.
        direction (str): The direction to move.

    Returns:
        (tuple<int, int>): Returns the row, column of the new position.
    """
    
    #To check the tile at the new position
    new_position = get_position_in_direction(position, direction)
    
    if get_tile_at_position(level, new_position) == WALL:
        while get_tile_at_position(level, new_position) != AIR:
            new_position = (new_position[0], new_position[1]+1)

    #To check the tile below the new position
    below_new_position = (new_position[0], new_position[1]-1)
    
    while get_tile_at_position(level, below_new_position) == AIR: 
        new_position = (new_position[0], new_position[1]-1)
        below_new_position = (new_position[0], new_position[1]-1)
            
    return new_position



def print_level(level, position):
    """Replaces the tile at the given level & position with the PLAYER tile.

    Parameters:
        level (str): The entire string of the level.
        position (tuple<int, int>): The row, column position of a tile.

    Returns:
        (str): The level string with the tile replaced
    """
    new_position = position_to_index(position,level_size(level))
    new_level = ''
    
    for i, j in enumerate(level):
        if i == new_position: #Add tile PLAYER if tile number equals new position
            new_level += PLAYER
        else: #Otherwise add all the tiles normally
            new_level += j
            
    print(new_level)


def attack(level, position):
    """Checks for the MONSTER tile and removes it if it is there.

    Parameters:
        level (str): The entire string of the level.
        position (tuple<int, int>): The row, column position of a tile.

    Returns:
        (str): The level string with the tile replaced if MONSTER tile is found
    """
    #To get and remove MONSTER from left position
    check_position_01 = (position[0]-1, position[1])
    position_01 = get_tile_at_position(level, check_position_01) #Convert tuple to int
    if position_01 == MONSTER:
        print("Attacking the monster on your left!")
        return remove_from_level(level, check_position_01)

    #To get and remove MONSTER from right position
    check_position_02 = (position[0]+1, position[1])
    position_02 = get_tile_at_position(level, check_position_02)#Convert tuple to int
    if position_02 == MONSTER:
        print("Attacking the monster on your right!")
        return remove_from_level(level, check_position_02)
    
    print("No monsters to attack!")
    return level

    

def tile_status(level, position):
    """
    Prints tile status if the game ends, and returns tile and
    level, updated if COIN or CHECKPOINT at the tile.

    Parameters:
        level (str): The entire string of the level.
        position (tuple<int, int>): The row, column position of a tile.

    Returns:
        (tuple<str, str>): The tile at position and the level string with
        the tile replaced in both if COIN or CHECKPOINT are found
    """
    tile_at_position = get_tile_at_position(level, position)
    
    if tile_at_position == GOAL:
        print("Congratulations! You finished the level")
    elif tile_at_position == MONSTER:
        print("Hit a monster!")
    elif tile_at_position == COIN or tile_at_position == CHECKPOINT:
        level = remove_from_level(level,position)
        
    return (tile_at_position, level)

def main():
    """
    Loads the level string from file, prints and keeps track of current score
    and latest level, and keeps asking for direction until the game ends.
    """
    file_name = input("Please enter the name of the level file (e.g. level1.txt): ")
    position = (0,1)
    level = load_level(file_name)
    SCORE_STR = 'Score: '
    score_int = 0
    direction = ''
    
    while direction != 'q':
        if direction == 'a':
            level = attack(level,position)
        elif direction == '?':
            print(HELP_TEXT)
            
        position = move(level, position, direction)
        if get_tile_at_position(level, position) == COIN:
            score_int += 1
            
        status_tuple = tile_status(level, position)
        level = status_tuple[1]
        
        if status_tuple[0] == GOAL or status_tuple[0] == MONSTER:
            direction = 'q'
        else:
            print(SCORE_STR + str(score_int))
            print_level(level, position)
            direction = input("Please enter an action (enter '?' for help): ")

if __name__ == "__main__":
    main()
