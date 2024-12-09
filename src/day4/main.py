import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
input_data = read_input(abs_path)

data = [list(line) for line in input_data.splitlines()]

# compute dimensions onces
rows = len(data)
cols = len(data[0])

# define search string
search_list = ['X', 'M', 'A', 'S']
search_length = len(search_list)

def get_next(row: int, col: int, direction: str) -> tuple[int, int]:
    if (direction == 'right'):
        col += 1
    elif (direction == 'down'):
        row += 1
    elif (direction == 'left'):
        col -= 1
    elif (direction == 'up'):
        row -= 1
    elif (direction == 'up-left'):
        row -= 1
        col -= 1
    elif (direction == 'up-right'):
        row -= 1
        col += 1
    elif (direction == 'down-left'):
        row += 1
        col -= 1
    elif (direction == 'down-right'):
        row += 1
        col += 1

    return row, col

directions = ['right', 'down', 'left', 'up', 'up-left', 'up-right', 'down-left', 'down-right']

# # find words
found = 0
for row in range(rows):
    for col in range(cols):
        char = data[row][col]

        if (char != search_list[0]):
            continue

        current_row = row
        current_col = col
        for direction in directions:
            for i in range(1, search_length):
                next = get_next(current_row, current_col, direction)

                # check out of bounds
                if (next[0] < 0 or next[0] >= rows or next[1] < 0 or next[1] >= cols):
                    # reset current row and col
                    current_row = row
                    current_col = col
                    break

                next_char = data[next[0]][next[1]]

                if (next_char != search_list[i]):
                    # reset current row and col
                    current_row = row
                    current_col = col
                    break

                if (i == search_length-1 and next_char == search_list[i]):
                    # reset current row and col
                    current_row = row
                    current_col = col
                    found += 1
                    break

                current_row = next[0]
                current_col = next[1]

print('Part 1: ', found)

mas_list = ['M', 'S']
mas_length = len(mas_list)
mas_directions = ['up-left', 'up-right']

def get_opposite(direction: str) -> str:
    if (direction == 'up-left'):
        return 'down-right'
    elif (direction == 'up-right'):
        return 'down-left'
    elif (direction == 'down-left'):
        return 'up-right'
    elif (direction == 'down-right'):
        return 'up-left'
    else: 
        raise ValueError('Invalid direction')
    

part2_found = 0
for row in range(rows):
    for col in range(cols):
        char = data[row][col]

        # quick and dirty because it's late and I want to sleep
        # look for 'A' only and check the 'X' conditions from there
        if (char != 'A'):
            continue

        mas_count = 0
        for direction in mas_directions:
            next = get_next(row, col, direction)

            if (next[0] < 0 or next[0] >= rows or next[1] < 0 or next[1] >= cols):
                continue

            next_char = data[next[0]][next[1]]

            if (next_char == 'M'):
                # find 'S' in the opposite direction
                opposite = get_opposite(direction)
                opposite_next = get_next(row, col, opposite)

                if (opposite_next[0] < 0 or opposite_next[0] >= rows or opposite_next[1] < 0 or opposite_next[1] >= cols):
                    continue

                opposite_char = data[opposite_next[0]][opposite_next[1]]

                if (opposite_char == 'S'):
                    mas_count += 1
                    continue

            if (next_char == 'S'):
                # find 'S' in the opposite direction
                opposite = get_opposite(direction)
                opposite_next = get_next(row, col, opposite)

                if (opposite_next[0] < 0 or opposite_next[0] >= rows or opposite_next[1] < 0 or opposite_next[1] >= cols):
                    continue

                opposite_char = data[opposite_next[0]][opposite_next[1]]

                if (opposite_char == 'M'):
                    mas_count += 1
                    continue

        if (mas_count == 2):
            part2_found += 1

print('Part 2: ', part2_found)