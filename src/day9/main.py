import sys
import os
from typing import List, Tuple
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input
from itertools import groupby

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
# abs_path = os.path.join(dir, 'example.txt')
input_data = read_input(abs_path)

EMPTY_SPACE = "."

def generate_map(input_data: str) -> List[str]:
    output = []

    for i, char in enumerate(input_data):
        is_file = i % 2 == 0
        
        for _ in range(int(char)):
            output.append(i // 2 if is_file else EMPTY_SPACE)

    return output

def format_disk(map: List[str]) -> None:
    gaps = []

    for i, char in enumerate(map):
        if char != EMPTY_SPACE:
            continue

        gaps.append(i)

    if not gaps:
        return

    is_formatting = True
    while is_formatting:
        # loop from the end of the disk map to find the first non-gap char
        for i in range(len(map)-1, -1, -1):
            if map[i] == EMPTY_SPACE:
                continue

            to_move = map[i]
            map[gaps[0]] = to_move
            map[i] = EMPTY_SPACE
            gaps.pop(0) # remove the just processed gap
            break  

        # exit condition is if the first occurence of a gap has only gaps after it until the end
        is_formatting = not all(char == EMPTY_SPACE for char in map[gaps[0]:])

def format_disk_part_2(map: List[str]) -> None:
    def _calculate_gaps(map: List[str]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int, str]]]:
        gaps: List[Tuple[int, int]] = []
        files: List[Tuple[int, int, str]] = []

        groups = groupby(map)
        running_index = 0
        for key, group in groups:
            length = len(list(group))

            if key == EMPTY_SPACE:
                gaps.append((length, running_index))
            else:
                files.append((length, running_index, key))

            running_index += length
        return (gaps, files)

    # Store a list of empty space sizes and positions (of the start of the sequence)
    # as well as a list of file sizes, positions and characters
    gaps, files = _calculate_gaps(map)

    if not gaps:
        return

    can_still_format = True
    while can_still_format:
        # check the last file in the list
        file_size, file_index, file_key = files.pop()

        # find a spot for it
        for i, (gap_size, gap_index) in enumerate(gaps):
            # move the file if it fits but only if we are moving the file to the left
            if gap_size >= file_size and gap_index < file_index:
                for j in range(file_size):
                    map[gap_index+j] = file_key
                    map[file_index+j] = EMPTY_SPACE
                
                # we found a spot so break out and process another file
                break
        
        # keep formatting until we've tried to shift each file once
        can_still_format = len(files) > 0

        if can_still_format:
            # Recalculating the gaps and files is expensive.
            # TODO: refactor to not require this.
            gaps, _ = _calculate_gaps(map)

def get_checksum(map: List[str]) -> int:
    checksum = 0
    for i, char in enumerate(map):
        if char == EMPTY_SPACE:
            continue

        checksum += i * int(char)

    return checksum

def process(input_data: str, part_2=False, print_results=False) -> int:
    disk_map = generate_map(input_data)

    # debugging
    if print_results:
        print(disk_map)

    if part_2:
        format_disk_part_2(disk_map)
    else:
        format_disk(disk_map)

    # debugging
    if print_results:
        print(disk_map)

    return get_checksum(disk_map)


print("Part 1: ", process(input_data))
print("Part 2: ", process(input_data, part_2=True))