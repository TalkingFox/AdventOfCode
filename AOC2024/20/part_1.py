import os
from typing import Dict, List, Set

input_path = os.path.join(os.path.dirname(__file__), "input.txt")


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)

    def __str__(self):
        return f"({self.x},{self.y})"


class CheatPoint(Point):
    def __init__(
        self,
        x: int,
        y: int,
        is_teleport_start: bool = False,
        is_teleport_end: bool = False,
    ):
        super().__init__(x, y)
        self.is_teleport_start = is_teleport_start
        self.is_teleport_end = is_teleport_end

    def add(self, other_point):
        return CheatPoint(self.x + other_point.x, self.y + other_point.y)

    @staticmethod
    def from_point(point: Point):
        return CheatPoint(point.x, point.y, is_teleport_start=False)


class Route(object):
    def __init__(self, points: List[CheatPoint]):
        self.points = points
        self.has_teleported = False
        self.total_time = len(self.points) - 1

    @staticmethod
    def from_route(route):
        new_points = list(route.points)
        route = Route(new_points)
        route.has_teleported = route.has_teleported
        return route

    def add_point(self, point: CheatPoint):
        self.total_time += 1
        self.points.append(point)
        if point.is_teleport_start:
            self.has_teleported = True

    def has_visited(self, point: CheatPoint) -> bool:
        return any(map(lambda x: x.x == point.x and x.y == point.y, self.points))


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


def print_route(map: List[List[str]], route: Route) -> None:
    clone_map = [x[:] for x in map]
    for point in route.points[1 : len(route.points) - 1]:
        if point.is_teleport_start:
            clone_map[point.y][point.x] = "1"
        elif point.is_teleport_end:
            clone_map[point.y][point.x] = "2"
        else:
            clone_map[point.y][point.x] = "O"

    for row in clone_map:
        print(f"".join(row))


def find_race_time(map: List[List[str]]) -> int:
    total_seconds = 0
    for row in map:
        for column in row:
            if column in [".", "E"]:
                total_seconds += 1
    return total_seconds


def find_standard_route(map: List[List[str]], start: Point) -> Route | None:
    root: Route = Route([CheatPoint.from_point(start)])
    increments = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
    visited_points: Set[str] = set()
    visited_points.add(str(start))

    while True:
        did_move = False
        for increment in increments:
            next_step = root.points[-1].add(increment)
            if next_step.x < 0 or next_step.y < 0:
                continue
            if next_step.y >= len(map) or next_step.x >= len(map[next_step.y]):
                continue
            if str(next_step) in visited_points:
                continue

            step_char = map[next_step.y][next_step.x]
            if step_char == "#":
                continue
            if step_char == "E":
                root.add_point(next_step)
                return root

            root.add_point(next_step)
            visited_points.add(str(next_step))
            did_move = True
            break

        if not did_move:
            return None


def find_time_saving_routes(
    map: List[List[str]], start: Point, time_to_save: int
) -> List[Route]:
    typical_route = find_standard_route(map, start)
    required_time = typical_route.total_time - time_to_save

    # build route cache using typical route
    route_by_position: Dict[str, Route] = {}
    for index, point in enumerate(typical_route.points):
        new_points = typical_route.points[index + 1 : len(typical_route.points)]
        route_by_position[str(typical_route.points[index])] = Route(new_points)

    cheated_walls = set()
    root: Route = Route([CheatPoint.from_point(start)])
    queue: List[Route] = [root]
    increments = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
    time_saving_routes: List[Route] = []

    while any(queue):
        node = queue.pop(0)
        if node.total_time >= required_time:
            continue

        for increment in increments:
            next_step = node.points[-1].add(increment)
            if next_step.x < 0 or next_step.y < 0:
                continue
            if next_step.y >= len(map) or next_step.x >= len(map[next_step.y]):
                continue
            if node.has_visited(next_step):
                continue

            next_step_key = str(next_step)
            if node.has_teleported and next_step_key in route_by_position:
                cached_route = route_by_position[next_step_key]
                if cached_route.total_time + node.total_time >= required_time:
                    continue
                combined_points = list(node.points)
                combined_points.extend(cached_route.points)
                combined_route = Route(combined_points)

                time_saving_routes.append(combined_route)
                continue

            step_char = map[next_step.y][next_step.x]
            if step_char == "#":
                if node.has_teleported:
                    continue
                if next_step_key in cheated_walls:
                    continue
                cheated_walls.add(next_step_key)
                next_step.is_teleport_start = True
                next_route: Route = Route.from_route(node)
                next_route.add_point(next_step)
                queue.append(next_route)
                continue

            if step_char == "E":
                node.add_point(next_step)
                time_saving_routes.append(node)
                continue

            next_route: Route = Route.from_route(node)
            next_route.add_point(next_step)
            queue.append(next_route)

    return time_saving_routes


print_map(grid)
print()

# typical_time = find_race_time(grid)
# print(f"Race takes {typical_time} picoseconds to complete")
time_to_save = 100
time_saving_routes = find_time_saving_routes(grid, start, time_to_save)
print(
    f"Found {len(time_saving_routes)} routes that save at least {time_to_save} picoseconds"
)
