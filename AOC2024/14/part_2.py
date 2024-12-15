from enum import Flag, auto
import os
from typing import Dict, List

# Notes on solution.
# I used the code below to print out the robot positions into a grid.
# From there, I -tailed an output file "robot_picture.txt" until I noticed any interesting patterns.
# I saw a strange formation at seconds 50 and 95.
# I also saw that similar structures repeated every 103 and 101 seconds respectively.
# Noticing that, I changed the function below to only print out values in those intervals.
# Eventually, on second 7569, the tree appeared.
# If no interesting patterns emerged from the -tail method, an approach of printing "interesting" positions based on robot clustering would have been considered.
# If an unusual number of robots were in a "contiguous" formation, that would be an indicator of an image being drawn.


class QuadrantFlag(Flag):
    NONE = auto()
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()

class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"
    
    def add(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)
    
    @staticmethod
    def from_str(text: str):
        split = text.split(",")
        return Point(int(split[0]), int(split[1]))

class Robot(object):
    def __init__(self, position: Point, velocity: Point):
        self.position = position
        self.velocity = velocity

robots: List[Robot] = []
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, 'r') as in_file:
    for line in in_file:
        if line == '\n':
            continue
        split = line.split()
        position = Point.from_str(split[0][2:])
        velocity = Point.from_str(split[1][2:])
        robot = Robot(position, velocity)
        robots.append(robot)
        
total_seconds = 100
map_size = Point(101,103)

def print_picture(robots: List[Robot]) -> None:
    drawing: List[List[str]] = [['.'] * map_size.x for i in range(map_size.y)]
    for robot in robots:
        drawing[robot.position.y][robot.position.x] = 'X'
    
    lines: List[str] = []
    for row in drawing:
        line = " ".join(row)
        lines.append(line)
    ascii = "\n".join(lines)
    with open(f'robot-picture.txt','w') as out_file:
        out_file.write(ascii)

second = 1
while True:
    for robot in robots:
        target_position = robot.position.add(robot.velocity)
        if target_position.x < 0:
            target_position.x = map_size.x + target_position.x
        if target_position.x >= map_size.x:
            target_position.x = target_position.x - map_size.x
        
        if target_position.y < 0:
            target_position.y = map_size.y + target_position.y
        if target_position.y >= map_size.y:
            target_position.y = target_position.y - map_size.y
        robot.position = target_position
    if second == 7569:
        print_picture(robots)
        input(f'Continue after second {second}?')
    second += 1