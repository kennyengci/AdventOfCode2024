from enum import Enum
import sys
import os
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
# abs_path = os.path.join(dir, 'example.txt')
# abs_path = os.path.join(dir, 'test.txt')
input_data = read_input(abs_path).splitlines()

class Operators(Enum):
    ADD = "+"
    MULTIPLY = "*"
    CONCATENATE = "||"

operations_part1 = [Operators.ADD, Operators.MULTIPLY]
operations_part2 = [Operators.ADD, Operators.MULTIPLY, Operators.CONCATENATE]

def resolve_operation(a: int, b: int, operation: Operators) -> int:
    if operation == Operators.ADD:
        return a + b
    elif operation == Operators.MULTIPLY:
        return a * b
    elif operation == Operators.CONCATENATE:
        return int(str(a) + str(b))
    else:
        raise ValueError("Invalid input")

def process(input: List[str], operations: List[Operators]) -> int:
    valid_sum = 0
    for line in input:
        sum_str, numbers_str = line.split(":")
        sum = int(sum_str)
        numbers = [int(num) for num in numbers_str.split()]

        tree: List[List[int]] = []
        for i,num in enumerate(numbers):
            if i == 0:
                tree.append([num])
                continue
            result = []
            for prev_num in tree[i-1]:
                for op in operations:
                    result.append(resolve_operation(prev_num, num, op))

            tree.append(result)

        # only check the deepest "nodes" of the tree 
        # as these are the figures that take all numbers into account
        if any(num == sum for num in tree[len(numbers)-1]):
            valid_sum += sum

    return valid_sum

print("Part 1: ", process(input_data, operations_part1))
print("Part 2: ", process(input_data, operations_part2))


            
                    
                 


