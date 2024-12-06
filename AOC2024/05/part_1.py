import os
from typing import Dict, List

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

page_sum = 0
for update in updates:
    is_correct = True
    for index, page in enumerate(update):
        if index == 0:
            continue
        
        predecessors = update[0:index]
        if page in illegal_predecessors_by_page:
            for predecessor in predecessors:
                if page in illegal_predecessors_by_page and predecessor in illegal_predecessors_by_page[page]:
                    is_correct = False
                    break

    if is_correct:
        middle_page = update[len(update) // 2]
        page_sum += middle_page

print(f'The sum of correct update pages is {page_sum}')
