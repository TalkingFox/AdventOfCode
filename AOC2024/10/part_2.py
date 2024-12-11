import os
from typing import List, Set


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'({self.x},{self.y})'


class Trail(object):
    def __init__(self, route: List[Point]):
        self.route = route

class Trailhead(object):
    def __init__(self, start: Point, trails: List[Trail]):
        self.start = start
        self.trails = trails
        self.rating = len(trails)
        
        self.score = 0
        unique_peaks = set()
        for trail in trails:
            peak = trail.route[-1]
            peak_str = str(peak)
            if peak_str in unique_peaks:
                continue
            unique_peaks.add(peak_str)
            self.score += 1


input_path = os.path.join(os.path.dirname(__file__), "input.txt")
grid: List[List[int]] = []
with open(input_path, "r") as in_file:
    active_row = []
    grid.append(active_row)
    while char := in_file.read(1):
        if char == "\n":
            active_row = []
            grid.append(active_row)
            continue
        active_row.append(int(char))

    grid = list(filter(lambda x: len(x) > 0, grid))


def follow_trail(grid: List[List[int]], start: Point, current_path: List[Point]) -> List[Trail]:
    start_value = grid[start.y][start.x]
    points_to_check: List[Point] = []
    if start.y > 0:
        points_to_check.append(Point(start.x, start.y - 1))
    if start.y < len(grid) - 1:
        points_to_check.append(Point(start.x, start.y + 1))
    if start.x > 0:
        points_to_check.append(Point(start.x - 1, start.y))
    if start.x < len(grid[start.y]) - 1:
        points_to_check.append(Point(start.x + 1, start.y))
    
    found_trails: List[Trail] = []
    for point in points_to_check:
        point_value = grid[point.y][point.x]
        if point_value != (start_value + 1):
            continue
        
        fork = list(current_path)
        
        if point_value == 9:
            fork.append(point)
            found_trail = Trail(fork)
            found_trails.append(found_trail)
            continue
        
        fork.append(point)
        fork_trails = follow_trail(grid, point, fork)
        if fork_trails:
            found_trails.extend(fork_trails)
    
    return found_trails


trailheads: List[Trailhead] = []
peaks_encountered: Set[str] = set()
for row_index, row in enumerate(grid):
    for column, character in enumerate(row):
        if character != 0:
            continue

        start_point = Point(column, row_index)
        start_path: List[Point] = [start_point]
        trails = follow_trail(grid, start_point, start_path)
        if trails:
            trailhead = Trailhead(start_point, trails)
            trailheads.append(trailhead)

print(f'{len(trailheads)} total trails found.')
rating_sum = 0
for trailhead in trailheads:
    rating_sum += trailhead.rating
print(f'The rating sum is {rating_sum}')