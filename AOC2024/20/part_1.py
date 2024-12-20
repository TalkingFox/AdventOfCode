import os
from typing import List

input_path = os.path.join(os.path.dirname(__file__), "input.txt")


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


grid: List[List[str]] = []
start: Point = None
end: Point = None
with open(input_path, "r") as in_file:
    active_row = []
    for row_index, row in enumerate(in_file):
        for column, char in enumerate(row):
            if char == "\n":
                grid.append(active_row)
                active_row = []
                continue
            if char == "S":
                start = Point(column, row_index)
            if char == "E":
                end = Point(column, row_index)
            active_row.append(char)

    if active_row:
        grid.append(active_row)


def print_map(map: List[List[str]]):
    for row in map:
        print(f"".join(row))


print_map(grid)
