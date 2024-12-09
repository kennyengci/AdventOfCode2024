import math
import sys
import os
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.libs.utils import read_input

dir = os.path.dirname(__file__)
abs_path = os.path.join(dir, 'input.txt')
input_data = read_input(abs_path)

rules = input_data.split('\n\n')[0].splitlines()
updates = input_data.split('\n\n')[1].splitlines()

valid_updates = [0 for _ in range(len(updates))] # initialise as zeroes
for i in range(len(updates)):
    update = updates[i]
    is_valid = True
    for rule in rules:
        rule_1, rule_2 = rule.split('|')

        rule_1_index = update.find(rule_1)
        rule_2_index = update.find(rule_2)

        # skip on missing candidates
        if rule_1_index == -1 or rule_2_index == -1:
            continue
            

        # fail
        if rule_2_index < rule_1_index:
            is_valid=False
            break

    # if we reach this point then all rules have passed, the update is valid
    if is_valid:
        valid_updates[i] = 1

# find middle value for each valid update
middle_values = []
for i in range(len(valid_updates)):
    if valid_updates[i] == 0:
        continue

    update_values = updates[i].split(',')

    # the updates always have an odd number of values
    middle_values.append(int(update_values[math.floor(len(update_values) / 2)]))

print('Part 1: ', sum(middle_values))

# Begin part 2
# take invalid updates from part 1 and fix them
invalid_updates = [update for i, update in enumerate(updates) if not valid_updates[i]]

fixed_updates: List[List[str]] = []
for i in range(len(invalid_updates)):
    update = invalid_updates[i].split(',')
    # we need to keep running through rules because one position swap can invalidate another rule within one pass
    done = False
    while (not done):
        touched = False
        for rule in rules:
            rule_1, rule_2 = rule.split('|')

            rule_1_index = update.index(rule_1) if update.__contains__(rule_1) else -1
            rule_2_index = update.index(rule_2) if update.__contains__(rule_2) else -1

            # skip on missing candidates
            if rule_1_index == -1 or rule_2_index == -1:
                continue

            if rule_2_index < rule_1_index:
                update[rule_1_index] = rule_2
                update[rule_2_index] = rule_1
                touched = True
        if not touched:
            done = True

    fixed_updates.append(update)

# find middle value for each fixed update
fixed_middle_values: List[int] = []
for i in range(len(fixed_updates)):
    update = fixed_updates[i]
    fixed_middle_values.append(int(update[math.floor(len(update) / 2)]))

print('Part 2: ', sum(fixed_middle_values))