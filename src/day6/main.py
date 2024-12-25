from enum import Enum
import sys
import os
from typing import List, Tuple
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
input_data = read_input(abs_path).splitlines()

GUARD = "^"

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

def next_coordinate(position: Tuple[int, int], dir: Direction) -> Tuple[int, int]:
    """

    Args:
        position (Tuple[int, int]): x , y coordinates
        dir (Directions): current direction the guard is facing, using the Direction enum

    Returns:
        Tuple[int, int]: the next coordinate the guard should enter
    """
    x = position[0]
    y = position[1]

    if dir == Direction.UP:
        y += 1
    elif dir == Direction.DOWN:
        y += -1
    elif dir == Direction.LEFT:
        x += -1
    elif dir == Direction.RIGHT:
        x += 1
    
    return x,y

def get_next_location(position: Tuple[int, int], map: List[str]):
    x_row = map[position[1]]
    location = x_row[position[0]]

    return location

def get_can_move(location: str) -> bool:
    if location == ".":
        return True
    # the initial location only matters during initialisation, it is equivalent to a "." afterwards
    if location == "^":
        return True
    elif location == "#":
        return False
    else:
        raise ValueError("Invalid input")

def turn(dir: Direction) -> Direction:
    if dir == Direction.UP:
        return Direction.RIGHT
    elif dir == Direction.DOWN:
        return Direction.LEFT
    elif dir == Direction.LEFT:
        return Direction.UP
    elif dir == Direction.RIGHT:
        return Direction.DOWN

is_in_map = True
x = None
y = None
direction = Direction.UP
x_limit = len(input_data[0])
y_limit = len(input_data)
visited: List[Tuple[int, int]] = []

input_data.reverse() # so we can have 0,0 as the bottom left of the map

# find initial position
for i, row in enumerate(input_data):
    index = row.find(GUARD)
    if index != -1:
        x = index
        y = i
        break

while (is_in_map):
    # store current location as visited
    current = x,y
    visited.append(current)

    # find the next coord
    next = next_coordinate(current, direction)
    # print('next', next)

    # end processing if we reach the edge of the map
    is_next_within_bounds = True if next[0] < x_limit and next[0] >= 0 and next[1] < x_limit and next[1] >= 0 else False
    if not is_next_within_bounds:
        is_in_map = False
        break

    # find what's in the next coord. E.g. obstruction
    next_location = get_next_location(next, input_data)

    # is it something that can be moved into?
    can_move = get_can_move(next_location)
    
    # move into the next spot if possible
    if can_move:
        x = next[0]
        y = next[1]
    # otherwise turn right
    else:
        direction = turn(direction)
        turn_next = next_coordinate(current, direction)
        # print('turn_next', turn_next)
        x = turn_next[0]
        y = turn_next[1]

unique_visited = list(set(visited))
print('Part 1: ', len(unique_visited))

