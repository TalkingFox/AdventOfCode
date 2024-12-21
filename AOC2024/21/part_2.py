import os
from typing import Generator, List, Set, Tuple


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)

    def equals(self, other_point) -> bool:
        return self.x == other_point.x and self.y == other_point.y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"


class Route(object):
    def __init__(self, route=None, start=None):
        self.directions: List[str] = []
        self.visited_nodes = set()
        self.cost = 0
        if start:
            self.position = start
            self.visited_nodes.add(str(start))
        if route:
            self.directions = route.directions.copy()
            self.position = route.position
            self.visited_nodes = route.visited_nodes.copy()
            self.cost = route.cost

    def move(self, direction: str, point: Point) -> None:
        self.directions.append(direction)

        price = 1 if self.position.x != point.x or self.position.y != point.y else 0
        self.cost += price

        self.position = point
        self.visited_nodes.add(point)

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


def calculate_button_sequence(
    button_map: List[List[str]], start_position: Point, code: str, limit: int = None
) -> List[Route]:
    cursor_position = start_position

    sequences: List[Route] = [Route(start=cursor_position)]

    for char in code:
        cheapest_sequences: List[Route] = []
        lowest_cost = None
        for sequence in sequences:
            paths = get_paths_to_character(button_map, sequence.position, char, limit)
            for path in paths:
                new_sequence = Route(sequence)
                new_sequence.visited_nodes.clear()
                new_sequence.directions.extend(path.directions)
                new_sequence.position = path.position
                new_sequence.cost += path.cost
                if lowest_cost == None:
                    lowest_cost = new_sequence.cost
                if lowest_cost > new_sequence.cost:
                    lowest_cost = new_sequence.cost
                    cheapest_sequences = []
                if lowest_cost == new_sequence.cost:
                    cheapest_sequences.append(new_sequence)
        sequences = cheapest_sequences

    return cheapest_sequences


# given a code, returns the optimal directional sequence required to press the buttons.
def calculate_num_button_sequences(code: str) -> List[Route]:
    grid: List[List[str]] = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        ["#", "0", "A"],
    ]
    start_position = Point(2, 3)
    return calculate_button_sequence(grid, start_position, code)


def calculate_dir_button_sequence(
    directions: List[str], limit: int = None
) -> List[Route]:
    grid: List[List[str]] = [
        ["#", "^", "A"],
        ["<", "v", ">"],
    ]
    start_position = Point(2, 0)
    code = "".join(directions)
    return calculate_button_sequence(grid, start_position, code, limit=limit)


sum_complexity = 0
chain_length = 2
for code in codes:
    num_sequences = calculate_num_button_sequences(code)
    next_level_sequences: List[Route] = num_sequences
    for i in range(chain_length):
        limit = 1 if (i + 1 == chain_length) else None
        queue: List[Route] = []
        for next_level_sequence in next_level_sequences:
            chain_sequences = calculate_dir_button_sequence(
                next_level_sequence.directions, limit
            )
            queue.extend(chain_sequences)
        next_level_sequences = queue
    
    cheapest_sequence = min(next_level_sequences, key=lambda x: x.cost)
    print("".join(cheapest_sequence.directions))
    numeric_code = int(code[0:3])
    local_complexity = len(cheapest_sequence.directions) * numeric_code
    sum_complexity += local_complexity

print(f"The sum complexity is {sum_complexity}")
