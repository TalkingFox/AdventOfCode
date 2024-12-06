import os
from typing import Dict, List

# Parse rules and updates from input
illegal_predecessors_by_page: Dict[int,List[int]] = {}
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
updates: List[List[int]] = []
with open(input_path, "r") as in_file:
    lines = in_file.readlines()
    finished_rules = False
    for line in lines:
        if line.isspace():
            finished_rules = True
            continue
        
        if not finished_rules:
            rule_split = line.split('|')
            key = int(rule_split[0])
            target = int(rule_split[1])
            if key not in illegal_predecessors_by_page:
                illegal_predecessors_by_page[key] = [target]
            else:
                illegal_predecessors_by_page[key].append(target)
            continue
        
        update = list(map(int, line.split(',')))
        updates.append(update)

# find illegal updates
illegal_updates: List[List[int]] = []
page_sum = 0
for update in updates:
    error_found = False
    for index, page in enumerate(update):
        if index == 0:
            continue
        
        predecessors = update[0:index]
        if page in illegal_predecessors_by_page:
            for predecessor in predecessors:
                if not page in illegal_predecessors_by_page:
                    continue
                
                if predecessor in illegal_predecessors_by_page[page]:
                    illegal_updates.append(update)
                    error_found = True
                    break
            
        if error_found:
            break
                
# sort the illegal updates
corrected_page_sums = 0
for illegal_update in illegal_updates:
    print(f'Changed {illegal_update}')
    index = 0
    while index < len(illegal_update):
        page = illegal_update[index]
        if index == 0:
            index += 1
            continue
        
        error_found = False
        predecessors = illegal_update[0:index]
        for predecessor_index, predecessor_page in enumerate(predecessors):
            if not page in illegal_predecessors_by_page:
                break
            if predecessor_page in illegal_predecessors_by_page[page]:
                # swap page with predecessor
                illegal_update[index] = predecessor_page
                illegal_update[predecessor_index] = page
                # must set index to predecessor in case of multiple rule violations.
                index = predecessor_index
                error_found = True
                break
        if not error_found:
            index += 1
    
    print(f'\t to {illegal_update}')
    corrected_page_sums += illegal_update[len(illegal_update) // 2]


print(f'The sum of corrected update pages is {corrected_page_sums}')