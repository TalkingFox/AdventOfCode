import os
from typing import Dict, List

class Node(object):
    def __init__(self, patterns: List[str]):
        self.patterns = patterns
        self.length = sum(map(lambda x: len(x),patterns))
        self.text = "".join(self.patterns)

available_patterns: List[str] = []
requested_designs: List[str] = []

input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    available_line = in_file.readline().split(",")
    available_patterns = list(map(lambda x: x.strip(), available_line))
    in_file.readline()

    for line in in_file:
        requested_designs.append(line.strip())


patterns_by_starting_color: Dict[str, List[str]] = {}
for pattern in available_patterns:
    start_color = pattern[0]
    if start_color not in patterns_by_starting_color:
        patterns_by_starting_color[start_color] = []
    patterns_by_starting_color[start_color].append(pattern)


def is_design_possible(design: str) -> bool:
    root_node = Node([])
    queue: List[Node] = [root_node]
    while any(queue):
        node = queue.pop()
        char_index = node.length
        char = design[char_index]
        if char not in patterns_by_starting_color:
            continue
        matches = patterns_by_starting_color[char]
        for match in matches:
            new_patterns = list(node.patterns)
            new_patterns.append(match)
            new_node = Node(new_patterns)
            if not new_node.text in design:
                continue
            if new_node.text == design:
                # print(f'{design} made with {new_node.patterns}')
                return True
            queue.append(new_node)
    
    return False

possible_designs = 0
for design in requested_designs:
    if is_design_possible(design):
        possible_designs += 1

print(f"{possible_designs} designs are possible.")
