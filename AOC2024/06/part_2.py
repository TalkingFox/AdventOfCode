import os
from typing import List, Tuple, Set, Dict
from enum import Enum


class GuardDirection(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


class Vector2(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (
            hasattr(other, "x")
            and hasattr(other, "y")
            and self.x == other.x
            and self.y == other.y
        )

    def __hash__(self):
        return hash((self.x, self.y))

    def add(self, other):
        return Vector2(self.x + other.x, self.y + other.y)


class DirectedVector2(Vector2):
    def __init__(self, x: int, y: int, direction: GuardDirection):
        super().__init__(x, y)
        self.direction = direction
    
    @staticmethod
    def copy(directed_vector):
        return DirectedVector2(directed_vector.x, directed_vector.y, directed_vector.direction)

    def add(self, other):
        return DirectedVector2(self.x + other.x, self.y + other.y, self.direction)
    
    def __eq__(self, other):
        return (
            hasattr(other, "x")
            and hasattr(other, "y")
            and hasattr(other, "direction")
            and self.x == other.x
            and self.y == other.y
            and self.direction == other.direction
        )
    
    def __hash__(self):
        return hash((self.x, self.y, self.direction))


guard_direction_by_character: dict[str, GuardDirection] = {
    "^": GuardDirection.North,
    ">": GuardDirection.East,
    "v": GuardDirection.South,
    "<": GuardDirection.West,
}

# read map, find current guard position and direction
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
input_grid: List[str] = []
guard_position: DirectedVector2 = None
current_direction: GuardDirection
with open(input_path, "r") as in_file:
    lines = in_file.readlines()
    for row, line in enumerate(lines):
        input_grid.append(line.strip())
        if guard_position != None:
            continue
        
        for column, character in enumerate(line):
            if character in guard_direction_by_character:
                current_direction = guard_direction_by_character[character]
                guard_position = DirectedVector2(column, row, current_direction)                
                break

# Simulate guard movement until exiting the map.
# Count the unique squares the guard visits
increment_by_direction = {
    GuardDirection.North: Vector2(0, -1),
    GuardDirection.East: Vector2(1, 0),
    GuardDirection.South: Vector2(0, 1),
    GuardDirection.West: Vector2(-1, 0),
}

direction_after_turning = {
    GuardDirection.North: GuardDirection.East,
    GuardDirection.East: GuardDirection.South,
    GuardDirection.South: GuardDirection.West,
    GuardDirection.West: GuardDirection.North,
}


def evaluate_guard_patrol(
    grid: List[str],
    starting_position: DirectedVector2,
) -> Tuple[bool, List[DirectedVector2]]:

    guard_position = DirectedVector2(starting_position.x, starting_position.y, starting_position.direction)
    unique_positions: Set[int] = set()
    
    visited_positions: List[DirectedVector2] = []
    visited_positions.append(DirectedVector2.copy(guard_position))

    # simulate guard movement
    while True:
        increment = increment_by_direction[guard_position.direction]
        target_position: DirectedVector2 = guard_position.add(increment)

        # assuming a fixed width grid
        is_target_on_map = 0 <= target_position.x < len(grid[0]) and 0 <= target_position.y < len(grid)
        if not is_target_on_map:
            break
        
        # check for obstacle
        rotate_count = 0
        while grid[target_position.y][target_position.x] == "#":
            rotate_count += 1
            if rotate_count == 4:
                return False, visited_positions
            target_position.direction = direction_after_turning[target_position.direction]
            guard_position.direction = target_position.direction
            increment = increment_by_direction[target_position.direction]
            target_position = guard_position.add(increment)

        guard_position = target_position
        visited_positions.append(target_position)
        
        # if the guard enters the same position from the same direction twice, they are looping
        # Not entirely sure why adding the classes directly to unique_positions wasn't working.
        # Need to better understand Python scope, I think.
        if guard_position.__hash__() in unique_positions:
            return False, visited_positions
        
        unique_positions.add(target_position.__hash__())

    return True, visited_positions


route_completes, patrol_route = evaluate_guard_patrol(input_grid, guard_position)
unique_positions: Set[Vector2] = set()
for directed_position in patrol_route:
    position = Vector2(directed_position.x, directed_position.y)
    unique_positions.add(position)
print(f"Guard visits {len(unique_positions)} unique locations. PathCompletes? {route_completes}")

obstacle_count = 0
# brute-force approach. Place an obstacle on each visited location.
# Can obtain substantial performance improvements by skipping chunks of positions where an obstacle will cause the guard to veer off the map.
# If there are any cycles in the approach (identified as a repeating sequence of visited positions), save it.
counter = 0
for position in unique_positions:
    if counter % 100 == 0:
        print(counter)
    if position.x == guard_position.x and position.y == guard_position.y:
        continue
    starting_position = DirectedVector2(guard_position.x, guard_position.y, guard_position.direction)
    clone_grid = list(input_grid)
    clone_grid[position.y] = clone_grid[position.y][:position.x] + '#' + clone_grid[position.y][position.x+1:]
    route_completes, patrol_route = evaluate_guard_patrol(clone_grid, starting_position)
    if not route_completes:
        # print(f'{position.x},{position.y}')
        obstacle_count += 1
    counter += 1
        
print(f'There are {obstacle_count} possible obstacle positions.')