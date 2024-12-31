import sys
import os
from typing import Dict, List, Tuple
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
# abs_path = os.path.join(dir, 'example.txt')
input_data = read_input(abs_path).splitlines()

def find_antenna_positions(map: List[str]) -> Dict[str, List[Tuple[int, int]]]:
    output: Dict[str, List[Tuple[int, int]]] = {}

    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == ".":
                continue
            elif char not in output:
                output[char] = []

            output[char].append((x, y))

    return output 

def find_antinodes(positions: Dict[str, List[Tuple[int, int]]], map_size: Tuple[int, int]) -> List[Tuple[int, int]]:
    output = []

    for antenna in positions.keys():
        # Lone antenna do not generate antinodes
        if len(positions[antenna]) <= 1:
            continue
        for current in positions[antenna]:
            for other in positions[antenna]:
                if current == other:
                    continue

                # find the vector from current antenna to other antenna
                vector = (other[0]-current[0], other[1]-current[1])

                # apply this same vector from the position of the other antenna to find one antinode
                antinode = (other[0] + vector[0], other[1] + vector[1])

                # check for out of bounds
                if (antinode[0] >= 0 and antinode[0] < map_size[0] and antinode[1] >= 0 and antinode[1] < map_size[1]):
                    output.append(antinode)


    return output

def find_antinodes_part_2(positions: Dict[str, List[Tuple[int, int]]], map_size: Tuple[int, int]) -> List[Tuple[int, int]]:
    output = []

    for antenna in positions.keys():
        # Lone antenna do not generate antinodes
        if len(positions[antenna]) <= 1:
            continue
        for current in positions[antenna]:
            # antenna themselves are antinodes, if at least one is present
            output.append(current)
            for other in positions[antenna]:
                if current == other:
                    continue

                # find the vector from current antenna to other antenna
                vector = (other[0]-current[0], other[1]-current[1])
                initial_vector = tuple(vector)

                # repeatedly apply this vector to find antinodes
                while True:
                    antinode = (other[0] + vector[0], other[1] + vector[1])

                    # check for out of bounds
                    if not (antinode[0] >= 0 and antinode[0] < map_size[0] and antinode[1] >= 0 and antinode[1] < map_size[1]):
                        break
                    
                    output.append(antinode)
                    x, y = initial_vector
                    vector = (vector[0] + x, vector[1] + y)

                # No need to apply vectors in the other direction as the loop will take care of that

    return output

def mark_antinodes_on_map(map: List[str], antinode_positions: List[Tuple[int, int]]) -> None:
    for position in antinode_positions:
        # check if antenna is not in this spot
        if map[position[1]][position[0]] != ".":
            continue
        
        original = map[position[1]]
        marked = f"{original[:position[0]]}#{original[position[0]+1:]}"
        map[position[1]] = marked

def print_map(map: List[str]) -> None:
    map_reversed = map.copy()
    map_reversed.reverse()

    for line in map_reversed:
        for char in line:
            print(char, end="")
        print("\n", end="")


def process(input_data: List[str], part_2=False) -> int:
    """_summary_

    Args:
        input_data (List[str]): input data straight from the web interface

    Returns:
        int: number of unique antinodes for the given input
    """

    map = input_data.copy()
    map.reverse() # Catesian coords: 0,0 is bottom left.

    marked_map = map.copy() # Copy of the input that we will mark/mutate our antinodes into.

    antenna_positions = find_antenna_positions(map)

    antinode_positions = None
    map_size = (len(map[0]), len(map))
    if part_2:
        antinode_positions = find_antinodes_part_2(antenna_positions, map_size)
    else:
        antinode_positions = find_antinodes(antenna_positions, map_size)

    unique_antinode_positions = set(antinode_positions)

    # for debugging
    mark_antinodes_on_map(marked_map, unique_antinode_positions)
    print_map(marked_map)

    return len(unique_antinode_positions)
    

print("Part 1: ", process(input_data))
print("Part 2: ", process(input_data, part_2=True))