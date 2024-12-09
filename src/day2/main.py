import sys
import os
from typing import Dict, List
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
input_data = read_input(abs_path).splitlines()

def check_safety(numbers: list[str]) -> bool:
    # todo optimize all this repetitive casting to int
    is_ascending =  all((int(next) > int(current)) and (int(next)-int(current) <= 3) for current, next in zip(numbers, numbers[1:]))
    is_descending = all(int(current) > int(next) and int(current)-int(next) <=3 for current, next in zip(numbers, numbers[1:]))

    if is_ascending or is_descending:
        return True
    else:
        return False


output = []
for i in range(len(input_data)):
    numbers = input_data[i].split()
    # print(numbers)
    # print([int(current) for current, next in zip(numbers, numbers[1:])])
    # print([int(next) for current, next in zip(numbers, numbers[1:])])
    # print('------')

    is_ascending =  all((int(next) > int(current)) and (int(next)-int(current) <= 3) for current, next in zip(numbers, numbers[1:]))
    is_descending = all(int(current) > int(next) and int(current)-int(next) <=3 for current, next in zip(numbers, numbers[1:]))

    if is_ascending or is_descending:
        output.append(1) # safe
    else:
        output.append(0)

print(sum(output)) # part 1 answer

# part 2 start
# Approach is to have each row generate permutations where one number is removed
# Generating data
numbers_dict: Dict[int, List[List[str]]] = {}
for i in range(len(input_data)):
    # make permutations where each array within the array has one number removed
    # add the initial array first
    permutations = [input_data[i].split()]

    # now loop through adding permutations
    for j in range(len(input_data[i].split())):
        current_permutation = input_data[i].split()
        current_permutation.pop(j)
        permutations.append(current_permutation)

    numbers_dict[i] = permutations
    
# now run the same algo across all permutations
part2_output = []
for key in numbers_dict.keys():
    safety_checks = [check_safety(numbers) for numbers in numbers_dict[key]]

    part2_output.append(1) if any(safety_checks) else output.append(0)

print(sum(part2_output)) # part 2 answer


    