import re
import sys
import os
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
input_data = read_input(abs_path)


def find_muls(input_data: str) -> List[str]:
    regex = r'mul\(\d{1,3},\d{1,3}\)'
    return re.findall(regex, input_data)

def parse_muls(muls: List[str]) -> List[int]:
    parsed_muls: List[int] = []

    for mul in muls:
        parsed_mul = mul.split('(')[1].split(')')[0].split(',')
        parsed_muls.append(int(parsed_mul[0]) * int(parsed_mul[1]))

    return parsed_muls

muls = find_muls(input_data)
parsed_muls = parse_muls(muls)

print('Part 1:', sum(parsed_muls))

def find_operations(input_data: str) -> List[str]:
    regex = r"do\(\)|don't\(\)|mul\(\d{1,3},\d{1,3}\)"
    return re.findall(regex, input_data)

def parse_operations(operations: List[str]) -> List[int]:
    valid_operations: List[int] = []

    is_do = True
    for operation in operations:
        if operation == 'do()':
            is_do = True
            continue
        if operation == 'don\'t()':
            is_do = False
            continue
        
        if is_do:
            print(operation)
            parsed = operation.split('(')[1].split(')')[0].split(',')
            valid_operations.append(int(parsed[0]) * int(parsed[1]))

    return valid_operations

operations = find_operations(input_data)
print(operations)
parsed_operations = parse_operations(operations)

print('Part 2:', sum(parsed_operations))


