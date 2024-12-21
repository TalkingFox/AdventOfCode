import os
from typing import Generator, List, Set, Tuple


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
        self.visited_nodes = set()
        if start:
            self.position = start
            self.visited_nodes.add(str(start))
        if route:
            self.directions = route.directions.copy()
            self.position = route.position
            self.visited_nodes = route.visited_nodes.copy()

    def move(self, direction: str, point: Point) -> None:
        self.directions.append(direction)
        self.position = point
        self.visited_nodes

    def has_visited(self, point: Point) -> bool:
        return str(point) in self.visited_nodes

    def __str__(self) -> str:
        return "".join(self.directions)


codes: List[str] = []
input_file = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file, "r") as in_file:
    for line in in_file:
        if line == "\n":
            continue
        codes.append(line.strip())


def get_paths_to_character(
    sub_grid: List[List[str]], start: Point, character: str, limit: int = None
) -> Generator[Route, None, None]:
    root = Route(start=start)
    if sub_grid[start.y][start.x] == character:
        root.move("A", root.position)
        yield root
        return
    queue: List[Route] = [root]
    increments: List[Tuple[str, Point]] = [
        ("^", Point(0, -1)),
        (">", Point(1, 0)),
        ("v", Point(0, 1)),
        ("<", Point(-1, 0)),
    ]
    returned_routes = 0
    best_distance: int = None
    while any(queue):
        node = queue.pop(0)
        if best_distance and len(node.directions) >= best_distance:
            continue
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

            if node.has_visited(next_position):
                continue
            next_node = Route(node)
            next_node.move(direction, next_position)
            if sub_grid[next_position.y][next_position.x] == character:
                next_node.move("A", next_position)
                yield next_node
                best_distance = len(next_node.directions) - 1
                returned_routes += 1
                if limit and returned_routes >= limit:
                    return
            queue.append(next_node)


# given a code, returns the optimal directional sequence required to press the buttons.
def calculate_button_sequences(code: str) -> List[Route]:
    grid: List[List[str]] = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        ["#", "0", "A"],
    ]
    cursor_position = Point(2, 3)

    sequences: List[Route] = [Route(start=cursor_position)]

    for char in code:
        new_sequences: List[Route] = []
        for sequence in sequences:
            paths = get_paths_to_character(grid, sequence.position, char)
            for path in paths:
                new_sequence = Route(sequence)
                new_sequence.visited_nodes.clear()
                new_sequence.directions.extend(path.directions)
                new_sequence.position = path.position
                new_sequences.append(new_sequence)
        sequences = new_sequences

    return sequences


def calculate_directional_sequence(directions: List[str]) -> List[str]:
    grid: List[List[str]] = [
        ["#", "^", "A"],
        ["<", "v", ">"],
    ]
    cursor_position = Point(2, 0)

    sequence: List[str] = []

    for char in directions:
        path_to_char = list(
            get_paths_to_character(grid, cursor_position, char, limit=1)
        )[0]
        sequence.extend(path_to_char.directions)
        cursor_position = path_to_char.position

    return sequence


print("029A")
sequences = calculate_button_sequences("029A")
for sequence in sequences:
    print(sequence)
    second_order_sequence = calculate_directional_sequence(sequence.directions)
    print("".join(second_order_sequence))
    third_order_sequence = calculate_directional_sequence(second_order_sequence)
    print("".join(third_order_sequence))
    print()
