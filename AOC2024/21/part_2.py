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
    else:
        target_difference = route.position.subtract(target)
        if abs(target_difference.x) == 1 and abs(target_difference.y) == 1:
            if target_difference.y < 0 and target_difference.x < 0:
                increment_y_first = True
            elif target_difference.y > 0 and target_difference.x < 0:
                increment_y_first = True

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


cache: Dict[str, Route] = {}


def calculate_dir_button_sequence(
    directions: List[str], depth: int, max_depth: int, start: Point = Point(2, 0)
) -> Route:
    # grid: List[List[str]] = [
    #     ["#", "^", "A"],
    #     ["<", "v", ">"],
    # ]

    route = Route(start=start)
    if depth == max_depth:
        early_route = Route(route)
        early_route.directions.extend(directions)
        return early_route

    panic = direction_index_by_character["#"]
    sub_route_position = route.position
    for char in directions:
        cache_key = f"{char}@{sub_route_position}@{depth}"
        if cache_key in cache:
            cache_route = cache[cache_key]
            route.directions.extend(cache_route.directions)
            route.position = cache_route.position
            continue
        target_point = direction_index_by_character[char]
        subroute = Route(start=sub_route_position)
        move_to_character(subroute, target_point, panic)
        sub_route_position = subroute.position
        next_level = calculate_dir_button_sequence(
            subroute.directions, depth + 1, max_depth, start=route.position
        )
        cache[cache_key] = Route(next_level)
        route.directions.extend(next_level.directions)
        route.position = next_level.position
    return route


sum_complexity = 0
chain_length = 2
for code in codes:
    button_route = calculate_num_button_sequences(code)
    print(button_route)
    chain_route = calculate_dir_button_sequence(
        button_route.directions, 0, max_depth=chain_length
    )
    print(f"{chain_route}")
    print()
    numeric_code = int(code[0:3])
    local_complexity = len(chain_route.directions) * numeric_code
    sum_complexity += local_complexity


print(f"The sum complexity is {sum_complexity}")