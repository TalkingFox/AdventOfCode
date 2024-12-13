from enum import Enum
import os, json
from typing import Dict, List, Set

input_path = os.path.join(os.path.dirname(__file__), "input.txt")

class Direction(Enum):
    NORTH = 1,
    EAST = 2
    SOUTH = 3
    WEST = 4    

class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def subtract(self, other_point):
        return Point(self.x - other_point.x, self.y - other_point.y)

class Wall(object):
    def __init__(self, direction: Direction, start_point: Point):
        self.direction = direction
        self.points: List[Point] = [start_point]
    
    def add_point(self, point: Point):
        self.points.append(point)
        
    def is_point_contiguous(self, new_point: Point) -> bool:
        for point in self.points:
            point_difference = point.subtract(new_point)
            if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
                if point_difference.y == 0 and abs(point_difference.x) == 1:
                    return True
            
            if self.direction == Direction.EAST or self.direction == Direction.WEST:
                if point_difference.x == 0 and abs(point_difference.y) == 1:
                    return True
        

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

    def count_sides(self) -> int:
        # collect lists of contiguous direction-facing walls
        wall_fragments_by_direction: Dict[Direction, List[Wall]] = {
            Direction.NORTH: [],
            Direction.EAST: [],
            Direction.SOUTH: [],
            Direction.WEST: []
        }
        for row_index, row in enumerate(self.grid):
            for column, character in enumerate(row):
                if character == '#':
                    continue
                
                current_point = Point(column, row_index)
                # check north
                if row_index <= 0 or self.grid[row_index-1][column] == '#':
                    fragment = Wall(Direction.NORTH, current_point)
                    wall_fragments_by_direction[Direction.NORTH].append(fragment)
                
                # check east
                if column >= len(self.grid[row_index])-1 or self.grid[row_index][column+1] == '#':
                    fragment = Wall(Direction.EAST, current_point)
                    wall_fragments_by_direction[Direction.EAST].append(fragment)
                
                # check south
                if row_index >= len(self.grid)-1 or self.grid[row_index+1][column] == '#':
                    fragment = Wall(Direction.SOUTH, current_point)
                    wall_fragments_by_direction[Direction.SOUTH].append(fragment)
                
                # check west
                if column <= 0 or self.grid[row_index][column-1] == '#':
                    fragment = Wall(Direction.WEST, current_point)
                    wall_fragments_by_direction[Direction.WEST].append(fragment)
        
        for direction, fragments in wall_fragments_by_direction.items():
            source_index = 0
            while source_index < len(fragments):
                source_fragment = fragments[source_index]
                compare_index = source_index+1
                while compare_index < len(fragments):
                    compare_fragment = fragments[compare_index]
                    # don't ever forget that at this point each wall only has one point.
                    if source_fragment.is_point_contiguous(compare_fragment.points[0]):
                        source_fragment.add_point(compare_fragment.points[0])
                        del fragments[compare_index]
                    else:
                        compare_index += 1
                source_index += 1
        total_sides = sum(len(fragments) for fragments in wall_fragments_by_direction.values())
        return total_sides


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
    sides = region.count_sides()
    # printables.append({
    #     'area': area,
    #     'sides': sides,
    # })
    total_cost += (area * sides)
    
# print(json.dumps(printables))
print(f'Total fencing costs: {total_cost}')