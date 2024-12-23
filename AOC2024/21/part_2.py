import os
from typing import Dict, Generator, List, Set, Tuple


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)

    def subtract(self, other_point):
        return Point(self.x - other_point.x, self.y - other_point.y)

    def equals(self, other_point) -> bool:
        return self.x == other_point.x and self.y == other_point.y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"


class Route(object):
    def __init__(self, route=None, start=None):
        self.directions: List[str] = []
        if start:
            self.position = start
        if route:
            self.directions = route.directions.copy()
            self.position = route.position
            self.route_length = route.route_length
        else:
            self.route_length = len(self.directions)

    def move(self, direction: str, point: Point) -> None:
        self.directions.append(direction)
        self.position = point

    def __str__(self) -> str:
        return "".join(self.directions)


codes: List[str] = []
input_file = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file, "r") as in_file:
    for line in in_file:
        if line == "\n":
            continue
        codes.append(line.strip())


def move_to_character(route: Route, target: Point, panic: Point) -> None:
    if route.position.equals(target):
        route.move("A", target)
        return

    increment_y_first = False
    if route.position.y == panic.y and target.x == panic.x:
        increment_y_first = True
    elif route.position.x == panic.x and target.y == panic.y:
        increment_y_first = False
    else:
        target_difference = route.position.subtract(target)
        if abs(target_difference.x) > 0 and abs(target_difference.y) > 0:
            # apply directional preferences
            # down-right
            if target_difference.y < 0 and target_difference.x < 0:
                increment_y_first = True
            # up-right
            elif target_difference.y > 0 and target_difference.x < 0:
                increment_y_first = True
            # otherwise, favor x increments first

    def increment_x():
        difference_x = route.position.x - target.x
        increment = 1 if difference_x < 0 else -1
        direction = ">" if increment == 1 else "<"
        while route.position.x != target.x:
            new_point = Point(route.position.x + increment, route.position.y)
            route.move(direction, new_point)

    if not increment_y_first:
        increment_x()

    difference_y = route.position.y - target.y
    increment = 1 if difference_y < 0 else -1
    direction = "v" if increment == 1 else "^"
    while route.position.y != target.y:
        new_point = Point(route.position.x, route.position.y + increment)
        route.move(direction, new_point)

    if increment_y_first:
        increment_x()
    route.move("A", target)


number_index_by_character: Dict[str, Point] = {
    "0": Point(1, 3),
    "1": Point(0, 2),
    "2": Point(1, 2),
    "3": Point(2, 2),
    "4": Point(0, 1),
    "5": Point(1, 1),
    "6": Point(2, 1),
    "7": Point(0, 0),
    "8": Point(1, 0),
    "9": Point(2, 0),
    "A": Point(2, 3),
    "#": Point(0, 3),
}

direction_index_by_character: Dict[str, Point] = {
    "#": Point(0, 0),
    "^": Point(1, 0),
    "A": Point(2, 0),
    "<": Point(0, 1),
    "v": Point(1, 1),
    ">": Point(2, 1),
}


# given a code, returns the optimal directional sequence required to press the buttons.
def calculate_num_button_sequences(code: str) -> List[Route]:
    # grid: List[List[str]] = [
    #     ["7", "8", "9"],
    #     ["4", "5", "6"],
    #     ["1", "2", "3"],
    #     ["#", "0", "A"],
    # ]

    start_position = Point(2, 3)
    route = Route(start=start_position)
    panic_point = number_index_by_character["#"]
    for char in code:
        target_point = number_index_by_character[char]
        move_to_character(route, target_point, panic_point)
    return route


class CacheEntry(object):
    def __init__(
        self,
        depth: int,
        char: str,
        subroute_position: Point,
        next_level_position: Point,
        route: Route,
    ):
        self.depth = depth
        self.char = char
        self.subroute_position = subroute_position
        self.next_level_position = next_level_position
        self.route = Route(route)
        # self.route.directions.clear()

    @staticmethod
    def get_key(
        depth: int, char: str, subroute_position: Point, next_level_position: Point
    ) -> str:
        return f"@{depth}&{char}&s{subroute_position}&n{next_level_position}"


cache: Dict[str, CacheEntry] = {}


def calculate_dir_button_sequence(
    directions: List[str], depth: int, max_depth: int, start: Point = Point(2, 0)
) -> Route:
    # grid: List[List[str]] = [
    #     ["#", "^", "A"],
    #     ["<", "v", ">"],
    # ]

    route = Route(start=start)

    # at max depth, don't expand the directions
    # return what you have
    if depth == max_depth:
        # route.directions.extend(directions)
        route.route_length += len(directions)
        return route

    panic = direction_index_by_character["#"]
    sub_route_position = Point(2, 0)
    next_level_position = Point(2, 0)
    for char in directions:
        cache_key = CacheEntry.get_key(
            depth, char, sub_route_position, next_level_position
        )
        if cache_key in cache:
            entry: CacheEntry = cache[cache_key]
            # route.directions.extend(entry.route.directions)
            route.route_length += entry.route.route_length
            route.position = entry.route.position
            next_level_position = entry.next_level_position
            sub_route_position = entry.subroute_position
            continue
        target_point = direction_index_by_character[char]
        subroute = Route(start=sub_route_position)
        move_to_character(subroute, target_point, panic)
        sub_route_position = subroute.position

        next_level = calculate_dir_button_sequence(
            subroute.directions, depth + 1, max_depth, start=route.position
        )

        entry: CacheEntry = CacheEntry(
            depth, char, sub_route_position, next_level.position, Route(next_level)
        )
        cache[cache_key] = entry
        # route.directions.extend(next_level.directions)
        route.route_length += next_level.route_length
        route.position = next_level.position
        next_level_position = next_level.position
    return route


sum_complexity = 0
chain_length = 25
for code in codes:
    button_route = calculate_num_button_sequences(code)
    print(button_route)
    chain_route = calculate_dir_button_sequence(
        button_route.directions, 0, max_depth=chain_length
    )
    # print(f"{chain_route.route_length}")
    # print(len(chain_route.directions))
    numeric_code = int(code[0:3])
    local_complexity = chain_route.route_length * numeric_code
    sum_complexity += local_complexity


print(f"The sum complexity is {sum_complexity}")
