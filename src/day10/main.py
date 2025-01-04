import sys
import os
from typing import List, Tuple
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input
from itertools import chain

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
# abs_path = os.path.join(dir, 'example.txt')
input = read_input(abs_path).splitlines()

def find_starting_positions(intput: List[str]) -> List[Tuple[int, int]]:
    output: List[Tuple[int, int]] = []

    for i, line in enumerate(input):
        for j, pos in enumerate(line):
            if pos == "0": 
                output.append((j, i))

    return output

def find_next_steps(gradient: int, current: Tuple[int, int], map: List[int]) -> List[Tuple[int, int]]:
    """
    Args:
        gradient (str): e.g. "0"
        map_size (Tuple[int, int]): (x , y) where x is map horizontal length and y is map height length
    """
    map_length = len(input[0])
    map_height = len(input)

    if gradient > 9:
        raise ValueError("Gradient provided is already at maximum")
    
    possible_steps = [(1,0), (0,1), (-1,0), (0,-1)]

    next_steps = [(current[0] + step[0], current[1] + step[1]) for step in possible_steps]
    next_steps = [step for step in next_steps if step[0] >= 0 and step[0] < map_length and step[1] >= 0 and step[1] < map_height ]
    next_steps = [step for step in next_steps if map[step[1]][step[0]] == str(gradient)]

    return next_steps

def solution(input: List[str]) -> int:
    starting_positions = find_starting_positions(input)
    trail_scores: List[int] = []

    for pos in starting_positions:
        next_gradient = 1
        next_steps = find_next_steps(next_gradient, pos, input)

        while next_steps:
            next_gradient += 1

            if next_gradient == 10:
                trail_scores.append(len(set(next_steps)))
                break

            next_steps = list(set(chain.from_iterable([find_next_steps(next_gradient, step, input) for step in next_steps])))

    return sum(trail_scores)

# Part two only differs from part one in that the `set` class is not used
def solution_part2(input: List[str]) -> int:
    starting_positions = find_starting_positions(input)
    trail_scores: List[int] = []

    for pos in starting_positions:
        next_gradient = 1
        next_steps = find_next_steps(next_gradient, pos, input)

        while next_steps:
            next_gradient += 1

            if next_gradient == 10:
                trail_scores.append(len(next_steps))
                break

            next_steps = list(chain.from_iterable([find_next_steps(next_gradient, step, input) for step in next_steps]))

    return sum(trail_scores)

print("Part 1: ", solution(input))
print("Part 2: ", solution_part2(input))