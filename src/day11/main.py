import functools
import sys
import os
from typing import List, Tuple
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
# abs_path = os.path.join(dir, 'example.txt')
# abs_path = os.path.join(dir, 'test.txt')
input = read_input(abs_path)

def solution(input: List[str], blinks: int) -> int:
    stones = [int(stone) for stone in input.split()]

    for _ in range(blinks):
        # track new inserts here and insert after completing the current loop
        # format is: (index, stone_number)
        new_stones: List[Tuple[int, int]] = [] 
        for j, stone in enumerate(stones):
            stone_str = str(stone)
            if stone == 0:
                stones[j] = 1
            elif len(stone_str) % 2 == 0:
                mid = len(stone_str) // 2
                stones[j] = int(stone_str[:mid])
                right = int(stone_str[mid:])
                new_stones.append((j+len(new_stones), right))
            else:
                stones[j] = stone * 2024
            

        for index, stone in new_stones:
            stones.insert(index + 1, stone)

    return len(stones)

print("Part 1: ", solution(input, 25))

# got a bit stuck on this part and turned to reddit for inspiration
@functools.cache
def blink(stone: int, times: int) -> int:
    stone_str = str(stone)

    # the final blink
    if times == 1:
        if stone == 0:
            return 1
        elif len(stone_str) % 2 == 0:
            return 2
        else:
            return 1
        
    if stone == 0:
        return blink(1, times-1)
    elif len(stone_str) % 2 == 0:
        mid = len(stone_str) // 2
        left = blink(int(stone_str[:mid]), times - 1)
        right = blink(int(stone_str[mid:]), times - 1)
        return left + right
    else:
        return blink(stone * 2024, times - 1)
    
def solution_part2(input: List[str], times: int) -> int:
    stones = [int(stone) for stone in input.split()]

    return sum(blink(stone, times) for stone in stones)

print("Part 2: ", solution_part2(input, 75))