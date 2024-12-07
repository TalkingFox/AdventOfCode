import os
from typing import List
from enum import Enum


class Vector2(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__ (self, other):
        return hasattr(other, 'x') and hasattr(other, 'y') and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash(str(self.x) + str(self.y))
    
    def add(self, other):
        return Vector2(self.x + other.x, self.y + other.y)


class GuardDirection(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

guard_direction_by_character: dict[str,GuardDirection] = {
    '^': GuardDirection.North,
    '>': GuardDirection.East,
    'v': GuardDirection.South,
    '<': GuardDirection.West
}

# read map, find current guard position and direction
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
grid: List[str] = []
guard_position: Vector2 = None
current_direction: GuardDirection
with open(input_path, "r") as in_file:
    lines = in_file.readlines()
    for row, line in enumerate(lines):
        grid.append(line.strip())
        for column, character in enumerate(line):
            if character in guard_direction_by_character:
                guard_position = Vector2(column, row)
                current_direction = guard_direction_by_character[character]
                break

        if guard_position != None:
            break
        
# Simulate guard movement until exiting the map.
# Count the unique squares the guard visits
increment_by_direction = {
    GuardDirection.North: Vector2(0,-1),
    GuardDirection.East: Vector2(1,0),
    GuardDirection.South: Vector2(0,1),
    GuardDirection.West: Vector2(-1,0)
}

direction_after_turning = {
    GuardDirection.North: GuardDirection.East,
    GuardDirection.East: GuardDirection.South,
    GuardDirection.South: GuardDirection.West,
    GuardDirection.West: GuardDirection.North
}

visited_locations = set()
visited_locations.add(guard_position)

while True:
    increment = increment_by_direction[current_direction]
    target_position = guard_position.add(increment)
    
    # assuming a fixed width grid
    is_target_on_map = 0 <= target_position.x < len(lines[0]) and 0 <= target_position.y < len(lines)
    if not is_target_on_map:
        break
    
    # check for obstacle
    # this will need to change if obstacle still exists after a turn
    if lines[target_position.y][target_position.x] == '#':
        current_direction = direction_after_turning[current_direction]
        increment = increment_by_direction[current_direction]
        target_position = guard_position.add(increment)
    
    guard_position =  target_position
    visited_locations.add(guard_position)

print(f'Guard visited {len(visited_locations)} unique locations.')