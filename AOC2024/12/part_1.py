import os
from typing import List, Set

input_path = os.path.join(os.path.dirname(__file__), "input.txt")


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

class Region(object):
    def __init__(self, width: int, height: int):
        self.grid = [['#'] * width for i in range(height)]
        self.area = 0
    
    def add(self, character: str, point: Point):
        self.area += 1
        self.grid[point.y][point.x] = character
        pass
    
    def __str__(self) -> str:
        return str(self.grid)


grid: List[List[str]] = []
with open(input_path, "r") as in_file:
    active_row = []
    while character := in_file.read(1):
        if character == "\n" and len(active_row) > 0:
            grid.append(active_row)
            active_row = []
            continue

        active_row.append(character)

def evaluate_region(
    source: List[List[str]], character: str, point: Point
) -> List[List[str]]:
    region = Region(len(grid[0]), len(grid))
    region.add(character, point)

    checked_points: Set[str] = set()
    points_to_check = [point]
    while len(points_to_check) > 0:
        point = points_to_check.pop()
        direction_points = [
            Point(point.x, point.y - 1),
            Point(point.x + 1, point.y),
            Point(point.x, point.y + 1),
            Point(point.x - 1, point.y),
        ]

        for direction_point in direction_points:
            if str(direction_point) in checked_points:
                continue
            if direction_point.x < 0 or direction_point.y < 0:
                continue
            if (
                direction_point.x > len(source[0]) - 1
                or direction_point.y > len(source) - 1
            ):
                continue

            new_character = source[direction_point.y][direction_point.x]
            if new_character == character:
                region.add(character, direction_point)
                source[direction_point.y][direction_point.x] = None
                points_to_check.append(direction_point)
                checked_points.add(str(direction_point))

    return region


regions = []
for row_index in range(len(grid)):
    for column_index in range(len(grid[row_index])):
        eval_character = grid[row_index][column_index]
        if eval_character == None:
            continue
        region = evaluate_region(grid, eval_character, Point(column_index, row_index))
        regions.append(region)

for region in regions:
    print(region)