import os
from typing import List

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f'({self.x},{self.y})'

class Machine(object):
    def __init__(self, a_increment: Point, b_increment: Point, prize_position: Point):
        self.a_increment = a_increment
        self.b_increment = b_increment
        self.prize_position = prize_position
    
    def __str__(self) -> str:
        return f'Button A: {self.a_increment}\nButton B: {self.b_increment}\nPrize: {self.prize_position}'

def read_button_increment(line: str) -> Point:
    x_index = 11
    comma_index = line.index(",")
    y_index = comma_index + 3
    x_increment = int(line[x_index:comma_index])
    y_increment = int(line[y_index:])
    return Point(x_increment, y_increment)

def read_prize_position(line: str) -> Point:
    x_index = 7
    comma_index = line.index(",")
    y_index = comma_index + 4
    x_position = int(line[x_index+2:comma_index])
    y_position = int(line[y_index:])
    return Point(x_position, y_position)

machines: List[Machine] = []
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, 'r') as in_file:
    while line := in_file.readline():
        a_increment = read_button_increment(line)
        
        b_line = in_file.readline()
        b_increment = read_button_increment(b_line)
        
        prize_line = in_file.readline().strip()
        prize_position = read_prize_position(prize_line)
        
        machine = Machine(a_increment, b_increment, prize_position)
        machines.append(machine)
        
        empty_line = in_file.readline()
        print(machine)
        print()