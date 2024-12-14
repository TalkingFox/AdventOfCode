from enum import Flag, auto
import os
from typing import Dict, List

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
for second in range(total_seconds):
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

robots_counts_by_quadrant: Dict[QuadrantFlag,int] = {}
x_midpoint = map_size.x // 2
y_midpoint = map_size.y // 2
for robot in robots:
    # ignore robots in the midpoints.
    if robot.position.x == x_midpoint or robot.position.y == y_midpoint:
        continue
    quadrant = QuadrantFlag.NONE
    quadrant |= QuadrantFlag.LEFT if robot.position.x < x_midpoint else QuadrantFlag.RIGHT
    quadrant |= QuadrantFlag.TOP if robot.position.y < y_midpoint else QuadrantFlag.BOTTOM
    if quadrant not in robots_counts_by_quadrant:
        robots_counts_by_quadrant[quadrant] = 0
    robots_counts_by_quadrant[quadrant] += 1

safety_factor = 1
for quadrant, count in robots_counts_by_quadrant.items():
    print(f'{quadrant} has {count} robots after {total_seconds} seconds') 
    safety_factor *= count

print(f'Safety factor is {safety_factor}')