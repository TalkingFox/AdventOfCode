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


class Route(object):
    def __init__(self, points: List[Point]):
        self.points = points
        self.total_time = len(self.points) - 1
        self.start_cheat_index: int = None
        self.end_cheat_index: int = None
        self.is_cheating: bool = False
        self.cheat_time: int = 0
        # self.visited_nodes: Set[str] = set(map(lambda x: str(x), points))

    @staticmethod
    def from_route(route):
        new_route = Route([])
        for point in route.points:
            new_route.add_point(point)
        new_route.start_cheat_index = route.start_cheat_index
        new_route.end_cheat_index = route.end_cheat_index
        new_route.is_cheating = route.is_cheating
        return new_route

    def add_point(self, point: Point) -> None:
        self.total_time += 1
        self.points.append(point)
        # self.visited_nodes.add(str(point))
        if self.is_cheating:
            self.cheat_time += 1

    def add_points(self, points: List[Point]) -> None:
        for point in points:
            self.add_point(point)

    def has_cheated(self):
        return self.end_cheat_index != None

    def activate_cheat(self):
        self.is_cheating = True
        self.start_cheat_index = len(self.points) - 1

    def deactivate_cheat(self):
        self.is_cheating = False
        self.end_cheat_index = len(self.points) - 1

    def get_cheat_key(self) -> str:
        start_cheat = self.points[self.start_cheat_index]
        end_cheat = self.points[self.end_cheat_index]
        return f"{start_cheat}-{end_cheat}"

    def has_visited(self, other_point: Point) -> bool:
        return False
        # return str(other_point) in self.visited_nodes


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
    cheat_index = 0
    should_count_cheats = False
    for index, point in enumerate(route.points[1 : len(route.points) - 1]):
        if should_count_cheats:
            cheat_index += 1
            clone_map[point.y][point.x] = str(cheat_index)

        clone_map[point.y][point.x] = "O"
        if index == route.start_cheat_index:
            should_count_cheats = True
        if index == route.end_cheat_index:
            should_count_cheats = False

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
    root: Route = Route([start])
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
    source_map: List[List[str]], start: Point, time_to_save: int, cheat_duration: int
) -> List[Route]:
    typical_route = find_standard_route(source_map, start)
    required_time = typical_route.total_time - time_to_save

    # build route cache using typical route
    route_by_position: Dict[str, Route] = {}
    point_index_by_point: Dict[str, int] = {}
    for index, point in enumerate(typical_route.points):
        new_points = typical_route.points[index + 1 : len(typical_route.points)]
        point_key = str(point)
        route_by_position[point_key] = Route(new_points)
        point_index_by_point[point_key] = index

    checked_points: Set[str] = set()
    time_saving_routes: List[Route] = []
    index = 1
    for point in typical_route.points:
        print(f"{index}/{typical_route.total_time}", end="\r")
        index += 1
        point_key = str(point)
        checked_points.add(point_key)
        # find all available points in a "duration"-radius from the starting point
        for column in range(-cheat_duration, cheat_duration + 1):
            for row in range(-cheat_duration, cheat_duration + 1):
                if row == 0 and column == 0:
                    continue
                if abs(column) + abs(row) > cheat_duration:
                    continue

                target_point = Point(point.x + column, point.y + row)
                if target_point.y < 0 or target_point.x < 0:
                    continue
                if target_point.y >= len(source_map) or target_point.x >= len(
                    source_map[row]
                ):
                    continue

                target_key = str(target_point)
                char = source_map[target_point.y][target_point.x]
                if char == "#":
                    continue

                if target_key in checked_points:
                    continue
                total_time = 0
                source_index = point_index_by_point[point_key]
                total_time += source_index

                # build route to target
                diff_y = abs(target_point.y - point.y)
                diff_x = abs(target_point.x - point.x)
                total_time += diff_x + diff_y

                if char != "E":
                    end_route = route_by_position[target_key]
                    total_time += end_route.total_time

                if total_time <= required_time:
                    time_saving_routes.append(Route([point, target_point]))
        # for each point in this radius, we already know the distance to the end.
        # from there, determine if it provides a reasonable cost-savings.

    return time_saving_routes


print()

# typical_time = find_race_time(grid)
# print(f"Race takes {typical_time} picoseconds to complete")
time_to_save = 100
cheat_duration = 20
time_saving_routes = find_time_saving_routes(grid, start, time_to_save, cheat_duration)
print(
    f"Found {len(time_saving_routes)} routes that save at least {time_to_save} picoseconds"
)
