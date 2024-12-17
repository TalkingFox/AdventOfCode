from enum import Enum
import os, sys
from typing import Dict, List

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


# depth-first search to find the lowest-scoring past to the endpoint
# depth-first search allows us to pre-emptively exit poor scoring paths if an optimal path is found first.
def evaluate_path(
    grid: List[List[str]],
    start: Step,
    current_path: List[Step],
    visited_points: set[Point],
    best_score: int = None,
) -> List[Step]:

    start_fork = list(current_path)
    start_fork.append(start)
    visited_fork = set(visited_points)
    visited_fork.add(str(start.point))

    # short-circuit known-worst paths
    if best_score != None and sum(map(lambda x: x.cost, start_fork)) >= best_score:
        return []

    # generate 5 possible next steps
    # 1 step forward (1 point)
    # 2 clockwise rotations (1000 points)
    # 2 counter-clockwise rotations (1000 points)
    forward_step = start.move_forward()
    step_char = grid[forward_step.point.y][forward_step.point.x]
    if step_char == "E":
        # don't bother checking other sibling points if the endpoint was found. They can't offer a better path.
        forward_step.mark_finished()
        start_fork.append(forward_step)
        visited_fork.add(str(forward_step.point))
        return start_fork

    best_route: List[Step] = []

    if step_char != "#" and str(forward_step.point) not in visited_fork:
        step_evaluation = evaluate_path(
            grid, forward_step, start_fork, visited_fork, best_score
        )
        if any(step_evaluation) and step_evaluation[-1].is_finished:
            step_score = sum(map(lambda x: x.cost, step_evaluation))
            if best_score == None or step_score < best_score:
                best_score = step_score
                best_route = step_evaluation

    # if last two steps were in the same place, do not generate rotations.
    # this implies a step of (1) - Landing on the square (2) - Rotating.
    # You will never need to rotate more than once.
    if len(start_fork) > 1 and start_fork[-1].point.equal(start_fork[-2].point):
        return best_route

    # note: for root node, it may be worth allowing the user to rotate a second time.
    # not currently implemented
    rotations = [
        start.clockwise_rotate(),
        start.counter_clockwise_rotate(),
    ]
    
    for rotation in rotations:
        rotation_evaluation = evaluate_path(
            grid, rotation, start_fork, visited_fork, best_score
        )
        if not any(rotation_evaluation):
            continue
        if not rotation_evaluation[-1].is_finished:
            continue
        rotation_score = sum(map(lambda x: x.cost, rotation_evaluation))
        if best_score == None or rotation_score < best_score:
            best_score = rotation_score
            best_route = rotation_evaluation

    return best_route


def draw_solved_map(grid: List[List[str]], steps: List[Step]) -> None:
    characters_by_direction = {
        Direction.NORTH: "^",
        Direction.EAST: ">",
        Direction.SOUTH: "v",
        Direction.WEST: "<",
    }
    copy_grid = [row[:] for row in grid]
    for step in steps[:-1]:
        if step.point.equal(steps[0].point):
            continue
        step_char = characters_by_direction[step.direction]
        copy_grid[step.point.y][step.point.x] = step_char

    for row in copy_grid:
        print(f'{"".join(row)}')
    score = sum(map(lambda x: x.cost, steps))
    print(f'Path score: {score}')


path = evaluate_path(grid, start_step, [], set())
draw_solved_map(grid, path)
