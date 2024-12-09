import sys
import os
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
input_data = read_input(abs_path)

left_list, right_list = zip(*(x.split() for x in input_data.splitlines()))
left_list = list(left_list)
right_list = list(right_list)

left_list = sorted(left_list)
right_list = sorted(right_list)

distances = []
for i in range(len(left_list)):
    distances.append(abs(int(left_list[i]) - int(right_list[i])))

# part 1 answer
print(sum(distances))

# part 2 start
left_occurances = [right_list.count(item) for item in left_list]
similarity_score = sum(int(item) * count for item, count in zip(left_list, left_occurances))
print(similarity_score)
