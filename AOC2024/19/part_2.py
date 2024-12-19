import os
from typing import Dict, List


class Node(object):
    def __init__(self, patterns: List[str]):
        self.patterns = patterns
        self.length = sum(map(lambda x: len(x), patterns))
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


arrangements_by_substring: Dict[str, int] = {}

def count_possible_arrangements(design: str) -> int:
    if design in arrangements_by_substring:
        return arrangements_by_substring[design]

    char = design[0]
    completed_arrangements = 0
    if char not in patterns_by_starting_color:
        arrangements_by_substring[design] = completed_arrangements
        return completed_arrangements
    matches = patterns_by_starting_color[char]
    for match in matches:
        if not design.startswith(match):
            continue
        if match == design:
            completed_arrangements += 1
            continue
        arrangements_from_here = count_possible_arrangements(design[len(match):])
        completed_arrangements += arrangements_from_here

    arrangements_by_substring[design] = completed_arrangements
    return completed_arrangements


possible_arrangements = 0
for index, design in enumerate(requested_designs):
    root_node = Node([])
    arrangements = count_possible_arrangements(design)
    possible_arrangements += arrangements
    print(arrangements)

print(f"{possible_arrangements} arrangements are possible.")