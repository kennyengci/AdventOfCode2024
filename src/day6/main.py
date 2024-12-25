from enum import Enum
import sys
import os
from typing import List, Tuple
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
# abs_path = os.path.join(dir, 'example.txt')
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

def find_visited(input_data: List[str]) -> List[Tuple[int, int]] | None:
    is_in_map = True
    x = None
    y = None
    direction = Direction.UP
    x_limit = len(input_data[0])
    y_limit = len(input_data)
    visited: List[Tuple[int, int]] = []
    move_count = 0
    move_limit = len(input_data) * len(input_data[0]) * 10

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

        # end processing if we reach the edge of the map
        is_next_within_bounds = True if next[0] < x_limit and next[0] >= 0 and next[1] < y_limit and next[1] >= 0 else False
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
            new_next = next_coordinate(current, direction)
            new_next_location = get_next_location(new_next, input_data)
            new_can_move = get_can_move(new_next_location)

            # if again we can't move, then basically do a 180deg turn
            # we should be able to move now
            if not new_can_move:
                direction = turn(direction)

            turn_next = next_coordinate(current, direction)
            x = turn_next[0]
            y = turn_next[1]
        
        move_count += 1
        # print('move_count: ', move_count)
        # assume guard is looping infinitely at this point
        if move_count >= move_limit:
            return None

    return visited

visited = find_visited(input_data.copy())
unique_visited = list(set(visited))
print('Part 1: ', len(unique_visited))

# Part 2 approach is to brute force try adding a "#" in each possible location (with no overlaps).
# Each time we simulate with the added obstruction we will move the guard until it has travelled 
# 10x the number of tiles on the map. I'm assuming that any valid path that would lead the guard to
# exit the map, would have done so before reaching this 10x limit *fingers crossed*.
# We can use the previously defined `find_visited` function, but count each simulation as a success if the function returns None,
# meaning the guard did not exit the map.

row_length = len(input_data[0])
column_length = len(input_data)
number_of_tiles = column_length * row_length
valid_cases: List[int] = []

for i in range(1, number_of_tiles):
    print(f'Processing index {i}...')
    def _modify_input(input_data: List[str], index: int) -> List[Tuple[int, int]] | None:
        modified_input_data = input_data.copy()

        # work from top left to bottom right.
        x = index % row_length - 1
        y = index // row_length 

        what_is_currently_there = modified_input_data[y][x]
        if what_is_currently_there == ".":
            row = list(modified_input_data[y])
            row[x] = "#"
            row_string = "".join(row)
            modified_input_data[y] = row_string
        if what_is_currently_there == "#":
            return None # don't process this as we will end up double counting
        if what_is_currently_there == "^":
            return None # invalid case

        return modified_input_data

    modified_input_data = _modify_input(input_data, i)
    if not modified_input_data:
        continue

    visited = find_visited(modified_input_data)

    if not visited:
        valid_cases.append(i)

print('Part 2: ', len(valid_cases))