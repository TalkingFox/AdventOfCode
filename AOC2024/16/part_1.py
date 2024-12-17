from enum import Enum
import os, sys
from typing import Dict, List, Set

sys.setrecursionlimit(10000)


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __hash__(self) -> int:
        return hash(str(self))

    def add(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)

    def equal(self, other_point) -> bool:
        return self.x == other_point.x and self.y == other_point.y


class Step(object):
    def __init__(self, point: Point, direction: Direction, cost: int):
        self.increment_by_direction = {
            Direction.NORTH: Point(0, -1),
            Direction.EAST: Point(1, 0),
            Direction.SOUTH: Point(0, 1),
            Direction.WEST: Point(-1, 0),
        }
        self.point = point
        self.cost = cost
        self.direction = direction
        self.is_finished = False

    def __hash__(self) -> int:
        return hash(f"{self.point}-{self.direction}")

    def clockwise_rotate(self):
        new_direction = Direction((self.direction.value + 1) % len(Direction))
        new_step = Step(self.point, new_direction, 1000)
        return new_step

    def counter_clockwise_rotate(self):
        new_direction = Direction((self.direction.value - 1) % len(Direction))
        new_step = Step(self.point, new_direction, 1000)
        return new_step

    def move_forward(self):
        increment = self.increment_by_direction[self.direction]
        new_point = self.point.add(increment)
        new_step = Step(new_point, self.direction, 1)
        return new_step

    def mark_finished(self) -> None:
        self.is_finished = True

class Route(object):
    def __init__(self, route = None):
        self.__visited_points__: Set[str] = set()
        self.steps: List[Step] = []
        self.score = 0
        if route:
            self.steps.extend(route.steps)
            self.score = route.score
            self.__visited_points__ = set(route.__visited_points__)
    
    def add(self, step: Step) -> None:
        self.steps.append(step)
        self.score += step.cost
    
    def has_visited(self, point: Point) -> bool:
        return str(point) in self.__visited_points__
    
    def just_rotated(self) -> bool:
        return len(self.steps) > 1 and self.steps[-1].point.equal(self.steps[-2].point)
    

def print_map(source: List[List[str]]) -> None:
    for row in source:
        print("".join(row))

start_position: Step = None
grid: List[List[str]] = []
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    active_row: List[str] = []
    for row_index, row in enumerate(in_file):
        if row == "\n":
            continue
        for column, char in enumerate(row):
            if char == "\n":
                grid.append(active_row)
                active_row = []
                continue
            if char == "S":
                start_point = Point(column, row_index)
                start_step = Step(start_point, Direction.EAST, 0)
            active_row.append(char)
    if len(active_row) > 0:
        grid.append(active_row)
        active_row = []


# breadth-first search to find the lowest-scoring past to the endpoint
# depth-first search allows us to pre-emptively exit all poor scoring paths as soon as an optimal path is found.
def evaluate_path(grid: List[List[str]],
    first_step: Step,
) -> Route:

    start_route = Route()
    start_route.add(first_step)
    route_queue: List[Route] = [start_route]
    best_route: Route = None
    explored_points_by_score: Dict[str, int] = {first_step.point: 0}
    while any(route_queue):
        root_route = route_queue.pop(0)
        # prune impossibly worse routes
        if best_route != None and root_route.score >= best_route.score:
            continue
            
        # generate 3 possible next steps
        # 1 step forward (1 point)
        forward_step = root_route.steps[-1].move_forward()
        
        step_char = grid[forward_step.point.y][forward_step.point.x]
        if step_char == "E":
            forward_route = Route(root_route)
            forward_route.add(forward_step)
            if best_route == None:
                best_route = forward_route
            elif forward_route.score < best_route.score:
                best_route = forward_route
            # don't generate sibling nodes. They won't be better.
            continue
        else:
            if not root_route.has_visited(forward_step.point) and step_char == '.':
                forward_route = Route(root_route)
                forward_route.add(forward_step)
                point_key = str(forward_step.point)
                if point_key not in explored_points_by_score or explored_points_by_score[point_key] >= forward_route.score:
                    # assumption: If one square has already been explored with a better score than you, your route is sub-optimal.
                    explored_points_by_score[point_key] = forward_route.score
                    route_queue.append(forward_route)
                
        # You will never rotate twice in a row.
        if root_route.just_rotated():
            continue
        
        # generate rotations
        # 1 clockwise rotations (1000 points)
        # 1 counter-clockwise rotations (1000 points)
        rotations = [
            root_route.steps[-1].clockwise_rotate(),
            root_route.steps[-1].counter_clockwise_rotate()
        ]
        for rotation in rotations:
            rotation_route = Route(root_route)
            rotation_route.add(rotation)
            route_queue.append(rotation_route)
            
    return best_route


def draw_solved_map(grid: List[List[str]], route: Route) -> None:
    characters_by_direction = {
        Direction.NORTH: "^",
        Direction.EAST: ">",
        Direction.SOUTH: "v",
        Direction.WEST: "<",
    }
    copy_grid = [row[:] for row in grid]
    for step in route.steps[:-1]:
        if step.point.equal(route.steps[0].point):
            continue
        step_char = characters_by_direction[step.direction]
        copy_grid[step.point.y][step.point.x] = step_char

    for row in copy_grid:
        print(f'{"".join(row)}')
    print(f"Path score: {route.score}")


path = evaluate_path(grid, start_step)
draw_solved_map(grid, path)
