import os
from typing import List, Set, Tuple


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)

    def __str__(self) -> str:
        return f"({self.x},{self.y})"


class Route(object):
    def __init__(self, route=None, start=None):
        self.directions: List[str] = []
        self.position = start
        if route:
            self.directions = list(route.directions)
            self.start = route.position

    def move(self, direction: str, point: Point) -> None:
        self.directions.append(direction)
        self.position = point


codes: List[str] = []
input_file = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file, "r") as in_file:
    for line in in_file:
        if line == "\n":
            continue
        codes.append(line.strip())


def get_path_to_character(
    sub_grid: List[List[str]], start: Point, character: str
) -> Route:
    root = Route(start=start)
    if sub_grid[start.y][start.x] == character:
        return root
    queue: List[Route] = [root]
    increments: List[Tuple[str, Point]] = [
        ("^", Point(0, -1)),
        (">", Point(1, 0)),
        ("v", Point(0, 1)),
        ("<", Point(-1, 0)),
    ]
    visited_points: Set[str] = set()
    while any(queue):
        node = queue.pop(0)
        for direction, increment in increments:
            next_position = node.position.add(increment)
            if next_position.x < 0 or next_position.y < 0:
                continue
            if next_position.y >= len(sub_grid) or next_position.x >= len(
                sub_grid[next_position.y]
            ):
                continue
            if sub_grid[next_position.y][next_position.x] == "#":
                continue

            next_position_key = str(next_position)
            if next_position_key in visited_points:
                continue
            visited_points.add(next_position_key)
            next_node = Route(node)
            next_node.move(direction, next_position)
            if sub_grid[next_position.y][next_position.x] == character:
                return next_node
            queue.append(next_node)
    return None


# given a code, returns the optimal directional sequence required to press the buttons.
def calculate_button_sequence(code: str) -> List[str]:
    grid: List[List[str]] = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        ["#", "0", "A"],
    ]
    cursor_position = Point(2, 3)

    sequence: List[str] = []

    for char in code:
        path_to_char = get_path_to_character(grid, cursor_position, char)
        sequence.extend(path_to_char.directions)
        sequence.append("A")
        cursor_position = path_to_char.position

    return sequence


def calculate_directional_sequence(directions: List[str]) -> List[str]:
    grid: List[List[str]] = [
        ["#", "^", "A"],
        ["<", "v", ">"],
    ]
    cursor_position = Point(2, 0)

    sequence: List[str] = []

    for char in directions:
        path_to_char = get_path_to_character(grid, cursor_position, char)
        sequence.extend(path_to_char.directions)
        sequence.append("A")
        cursor_position = path_to_char.position

    return sequence


sequence = calculate_button_sequence("029A")
print(sequence)
second_order_sequence = calculate_directional_sequence(sequence)
print(second_order_sequence)
