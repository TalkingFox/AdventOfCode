import os
from typing import List, Set


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def add(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)

    def equals(self, other_point) -> bool:
        return self.x == other_point.x and self.y == other_point.y


class Route(object):
    def __init__(self, points: List[Point]):
        self.points = points


def print_map(map: List[List[str]], route: Route = None) -> None:
    copy_map = map
    if route:
        copy_map = [x[:] for x in map]
        for point in route.points:
            copy_map[point.y][point.x] = "O"

    for row in copy_map:
        print("".join(row))


map_size = Point(71, 71)
grid: List[List[str]] = [["."] * map_size.x for x in range(map_size.y)]
byte_positions: List[Point] = []


input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    bytes_read = 0
    for row in in_file:
        if row == "\n":
            continue
        split = row.split(",")
        position = Point(int(split[0]), int(split[1]))
        byte_positions.append(position)
        bytes_read += 1


def place_bytes(map: List[List[str]], bytes: List[Point], bytes_to_read: int) -> None:
    for position in byte_positions[:bytes_to_read]:
        map[position.y][position.x] = "#"


def find_best_route(map: List[List[str]], start: Point, exit: Point) -> Route | None:
    root_node: Route = Route([start])
    queue: List[Route] = [root_node]
    directional_increments = {Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)}
    explored_points: Set[str] = set()

    while any(queue):
        node = queue.pop(0)
        node_start = node.points[-1]
        if str(node_start) in explored_points:
            continue
        explored_points.add(str(node_start))
        # generate next steps
        for increment in directional_increments:
            next_step = node_start.add(increment)
            if next_step.x < 0 or next_step.y < 0:
                continue
            if next_step.y >= len(map) or next_step.x >= len(map[next_step.y]):
                continue
            step_char = map[next_step.y][next_step.x]
            if step_char == "#":
                continue

            new_points = list(node.points)
            new_points.append(next_step)
            new_route = Route(new_points)
            if next_step.equals(exit):
                return new_route
            queue.append(new_route)

    return None


def find_byte_of_doom(
    map: List[List[str]], start: Point, exit: Point, byte_positions: List[Point]
) -> Point:
    # binary search to find which byte index is the earliest doomed index
    floor = 0
    ceiling = len(byte_positions) - 1
    while True:
        working_map = [x[:] for x in map]
        index_to_check = (floor + ceiling) // 2
        place_bytes(working_map, byte_positions, index_to_check + 1)
        best_route = find_best_route(working_map, start, exit)
        if best_route == None:
            ceiling = index_to_check
        else:
            floor = index_to_check
        if ceiling - floor == 1:
            return byte_positions[ceiling]


byte_of_doom = find_byte_of_doom(
    grid, Point(0, 0), map_size.add(Point(-1, -1)), byte_positions
)
print(f"The byte of doom falls at {str(byte_of_doom)}")
