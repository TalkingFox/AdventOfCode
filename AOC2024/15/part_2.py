import os
from typing import Dict, List, Tuple


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)

    def __str__(self) -> str:
        return f"({self.x},{self.y})"
    
    def __hash__(self) -> int:
        return hash(str(self))


grid: List[List[str]] = []
instructions: List[str] = []
input_file = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file, "r") as in_file:
    # read map
    for row_index, row in enumerate(in_file):
        if row.isspace():
            break
        grid_row: List[str] = []
        grid.append(grid_row)
        for column, char in enumerate(row):
            if char == "\n":
                continue
            match char:
                case "@":
                    start_position = Point(len(grid_row), row_index)
                    grid_row.append(char)
                    grid_row.append(".")
                case "O":
                    grid_row.append("[")
                    grid_row.append("]")
                case _:
                    grid_row.append(char)
                    grid_row.append(char)

    if start_position == None:
        raise Exception("Robot not found in map.")

    # read movement instructions
    while instruction := in_file.read(1):
        if instruction == "\n":
            continue
        instructions.append(instruction)


def print_grid(source: List[List[str]]):
    for row in source:
        print("".join(row))


increments_by_instruction = {
    ">": Point(1, 0),
    "v": Point(0, 1),
    "<": Point(-1, 0),
    "^": Point(0, -1),
}


def move_robot(grid: List[List[str]], start_position: Point, instruction: str) -> Point:
    robot_position = start_position
    increment = increments_by_instruction[instruction]
    target_position = robot_position.add(increment)
    target_tile = grid[target_position.y][target_position.x]

    # Move onto empty space
    if target_tile == ".":
        grid[robot_position.y][robot_position.x] = "."
        grid[target_position.y][target_position.x] = "@"
        robot_position = target_position
        return robot_position

    # Don't move if bump into wall
    if target_tile == "#":
        return robot_position

    # Try to push box
    if target_tile in ["[", "]"]:

        # check if box is pushable
        # is there anything on the other side of the box?
        if increment.y == 0:
            box_positions: List[Tuple[Point,str]] = [(target_position,target_tile)]                        
            beyond_box_point = target_position.add(increment)
            beyond_box_tile = grid[beyond_box_point.y][beyond_box_point.x]
            while beyond_box_tile in ["[", "]"]:
                box_positions.append((beyond_box_point,beyond_box_tile))
                beyond_box_point = beyond_box_point.add(increment)
                beyond_box_tile = grid[beyond_box_point.y][beyond_box_point.x]

            # cannot push boxes through a wall
            if beyond_box_tile == "#":
                return robot_position

            # otherwise, the tile is a '.' and all sequential boxes may be pushed
            grid[robot_position.y][robot_position.x] = "."
            robot_position = robot_position.add(increment)
            grid[robot_position.y][robot_position.x] = "@"
            
            for (box_position,box_char) in box_positions:
                new_position = box_position.add(increment)
                grid[new_position.y][new_position.x] = box_char
            return robot_position
        else:
            moving_boxes: List[Tuple[Point,str]] = [(target_position, target_tile)]
            check_increment = increments_by_instruction[">"] if target_tile == '[' else increments_by_instruction['<']
            check_position = target_position.add(check_increment)
            check_char = grid[check_position.y][check_position.x]
            moving_boxes.append((check_position,check_char))
            
            # for each box tile in moving boxes, check if there is a box one increment above it. 
            index = 0
            while index < len(moving_boxes):
                (box_position, box_char) = moving_boxes[index]
                check_position = box_position.add(increment)
                check_tile = grid[check_position.y][check_position.x]
                if check_tile == '#':
                    return robot_position
                
                if check_tile == '.':
                    index += 1
                    continue
                
                if check_tile in ['[',']']:
                    moving_boxes.append((check_position,check_tile))
                    check_increment = increments_by_instruction['>'] if check_tile == '[' else increments_by_instruction['<']
                    check_position = check_position.add(check_increment)
                    check_tile = grid[check_position.y][check_position.x]
                    moving_boxes.append((check_position, check_tile))
                    index += 1
                    continue
                
                index += 1
            
            # clear out all box tiles
            for moving_box in moving_boxes:
                (box_position, box_char) = moving_box
                grid[box_position.y][box_position.x] = '.'
                
            # Then move all box tiles one increment.
            for moving_box in moving_boxes:
                (box_position, box_char) = moving_box
                new_position = box_position.add(increment)
                grid[new_position.y][new_position.x] = box_char
            
            # Finally, place the robot in their new position
            grid[robot_position.y][robot_position.x] = '.'
            robot_position = robot_position.add(increment)
            grid[robot_position.y][robot_position.x] = '@'
                
            return robot_position
    return robot_position


print("Initial state")
print_grid(grid)
print(f"Robot Position: {start_position}")
current_position = start_position
for instruction in instructions:
    # print(f'Move {instruction}:')
    current_position = move_robot(grid, current_position, instruction)
    # print_grid(grid)

print_grid(grid)
coordinate_sum = 0
for row_index, row in enumerate(grid):
    for column, char in enumerate(row):
        if char == "[":
            gps_value = (100 * row_index) + column
            coordinate_sum += gps_value
print(f"Coordinate sum is {coordinate_sum}")
