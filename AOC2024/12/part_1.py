import os, json
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
        self.grid = [['#'] * width for i in range(height+1)]
        self.area = 0
    
    def add(self, character: str, point: Point):
        self.area += 1
        self.grid[point.y][point.x] = character
        pass
    
    def __str__(self) -> str:
        return str(self.grid)
    
    def calculate_perimiter(self) -> int:
        total_perimeter = 0
        for row_index, row in enumerate(self.grid):
            for column, character in enumerate(row):
                if character == '#':
                    continue
                directions = [
                    Point(column, row_index - 1),
                    Point(column + 1, row_index),
                    Point(column, row_index + 1),
                    Point(column - 1, row_index)
                ]
                for direction in directions:
                    if direction.x < 0 or direction.y < 0:
                        total_perimeter += 1
                        continue
                    if direction.x > len(row)-1 or direction.y > len(self.grid)-1:
                        total_perimeter += 1
                        continue
                    check_character = self.grid[direction.y][direction.x]
                    if check_character == '#':
                        total_perimeter += 1
        
        return total_perimeter


grid: List[List[str]] = []
with open(input_path, "r") as in_file:
    active_row = []
    while character := in_file.read(1):
        if character == "\n" and len(active_row) > 0:
            grid.append(active_row)
            active_row = []
            continue

        active_row.append(character)
    if active_row:
        grid.append(active_row)

def evaluate_region(
    source: List[List[str]], character: str, point: Point
) -> List[List[str]]:
    region = Region(len(grid[0]), len(grid))
    region.add(character, point)

    checked_points: Set[str] = set()
    checked_points.add(str(point))
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


regions: List[Region] = []
for row_index in range(len(grid)):
    for column_index in range(len(grid[row_index])):
        eval_character = grid[row_index][column_index]
        if eval_character == None:
            continue
        region = evaluate_region(grid, eval_character, Point(column_index, row_index))
        regions.append(region)

printables = []
total_cost = 0
for region in regions:
    area = region.area
    perimiter = region.calculate_perimiter()
    # printables.append({
    #     'area': area,
    #     'perimeter': perimiter,
    # })
    # print(str(region))
    total_cost += (area * perimiter)
    
# print(json.dumps(printables))
print(f'Total fencing costs: {total_cost}')