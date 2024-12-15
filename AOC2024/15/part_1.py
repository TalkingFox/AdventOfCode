import os
from typing import List 

class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def add(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)

grid: List[List[str]] = []
instructions: List[str] = []
start_position: Point = None
input_file = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file, 'r') as in_file:
    # read map
    for row_index, row in enumerate(in_file):
        if row.isspace():
            break
        grid_row: List[str] = []
        grid.append(grid_row)
        for column, char in enumerate(row):
            if char == '\n':
                continue
            grid_row.append(char)
            if char == '@':
                start_position = Point(column, row_index)
    
    if start_position == None:
        raise Exception("Robot not found in map.")
    
    # read movement instructions
    while instruction := in_file.read(1):
        if instruction == '\n':
            continue
        instructions.append(instruction)

def print_grid(source: List[List[str]]):
    for row in source:
        print("".join(row))
        
increments_by_instruction = {
    '>': Point(1,0),
    'v': Point(0,1),
    '<': Point(-1,0),
    '^': Point(0,-1)
}
robot_position = start_position

def move_robot(grid: List[List[str]], start_position: Point, instruction: str) -> Point:
    robot_position = start_position
    increment = increments_by_instruction[instruction]
    target_position = robot_position.add(increment)
    target_tile = grid[target_position.y][target_position.x]
    
    # Move onto empty space
    if target_tile == '.':
        grid[robot_position.y][robot_position.x] = '.'
        grid[target_position.y][target_position.x] = '@'
        robot_position = target_position
        return robot_position
    
    # Don't move if bump into wall
    if target_tile == '#':
        return robot_position
    
    # Try to push box
    if target_tile == 'O':
        box_positions = [target_position]
        
        # check if box is pushable
        # is there anything on the other side of the box?
        beyond_box_point = target_position.add(increment)
        beyond_box_tile = grid[beyond_box_point.y][beyond_box_point.x]
        while beyond_box_tile == 'O':
            box_positions.append(beyond_box_point)
            beyond_box_point = beyond_box_point.add(increment)
            beyond_box_tile = grid[beyond_box_point.y][beyond_box_point.x]

        # cannot push boxes through a wall
        if beyond_box_tile == '#':
            return robot_position
        
        # otherwise, the tile is a '.' and all sequential boxes may be pushed
        grid[robot_position.y][robot_position.x] = '.'
        robot_position = robot_position.add(increment)
        grid[robot_position.y][robot_position.x] = '@'
        grid_cursor = robot_position
        for box_position in box_positions:
            grid_cursor = grid_cursor.add(increment)
            grid[grid_cursor.y][grid_cursor.x] = 'O'
    
    return robot_position
            

print("Initial state")
print_grid(grid)
current_position = start_position
for instruction in instructions:
    current_position = move_robot(grid, current_position, instruction)

coordinate_sum = 0
for row_index, row in enumerate(grid):
    for column, char in enumerate(row):
        if char == 'O':
            gps_value = (100 * row_index) + column
            coordinate_sum += gps_value
print(f'Coordinate sum is {coordinate_sum}')