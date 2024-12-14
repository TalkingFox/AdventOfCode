import os
from typing import List, Tuple


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"


class Variable(object):
    def __init__(self, modifier: int, character: str = ''):
        self.modifier = modifier
        self.character = character

    def evaluate(self, value: int) -> int:
        return self.modifier * value

    def __str__(self) -> str:
        return f"{self.modifier}{self.character}"
    
    def subtract(self, other_variable):
        if other_variable.character != self.character:
            raise Exception(f"Cannot subtract {other_variable.character} from {self.character}")
        
        return Variable(self.modifier - other_variable.modifier, self.character)

    def divide(self, value: int):
        return Variable(self.modifier / value, self.character)


class Expression(object):
    def __init__(self, left_side: List[Variable], right_side: List[Variable]):
        self.left_side = left_side
        self.right_side = right_side

    def __str__(self) -> str:
        return f'{"+".join(map(str,self.left_side))}={"+".join(map(str,self.right_side))}'
    
    def combine(self, other_expression) -> Tuple[Variable, Variable]:
        # Key Assumptions: that both expressions have the same number of variables on their left and right sides.
        # Both expressions are in the format ax + by = c.
        
        working_self: Expression = self.multiply(1)
        # multiply the first expression by the modifier of the first variable of the second expression
        this_mult_value = self.left_side[0].modifier
        other_mult_value = other_expression.left_side[0].modifier
        working_self = working_self.multiply(other_mult_value)
        
        # multiply the second expression by the modifier of the first variable of the first expression
        other_expression = other_expression.multiply(this_mult_value)
        
        # subtract the second expression from the first expression. A new expression will be the result.
        new_left_side = []
        for i in range(len(working_self.left_side)):
            new_variable = working_self.left_side[i].subtract(other_expression.left_side[i])
            if new_variable.modifier == 0:
                continue
            new_left_side.append(new_variable)
        
        new_right_side = []
        for i in range(len(working_self.right_side)):
            new_variable = working_self.right_side[i].subtract(other_expression.right_side[i])
            new_right_side.append(new_variable)
        
        new_expression = Expression(new_left_side, new_right_side)
        
        # Get the value of Y by dividing both sides of the expression by the modifier of y.
        if len(new_expression.left_side) > 1 or len(new_expression.right_side) > 1:
            raise Exception("Cannot divide for value of y unless both sides of the expression have the same number of components")
        y_divisor = new_expression.left_side[0].modifier
        new_left = [new_expression.left_side[0].divide(y_divisor)]
        new_right = [new_expression.right_side[0].divide(y_divisor)]
        new_expression = Expression(new_left, new_right)
        if new_expression.left_side[0].modifier != 1:
            raise Exception("Y should be equal to 1 at this point")
        y_value = new_expression.right_side[0].modifier
        
        # if y is non-integer, return none.
        if y_value % 1 != 0:
            return None
        
        # otherwise, substitute the value of y into the first expression and solve for x.
        x_expression = self.substitute('y', y_value)
        y_constant = x_expression.left_side[1]
        other_constant = x_expression.right_side[0].subtract(y_constant)
        x_variable = x_expression.left_side[0]
        x_value = other_constant.divide(x_variable.modifier).modifier
        
        # if x is non-integer, return None.
        if x_value % 1 != 0:
            return None
        
        # otherwise, return (x,y)
        return x_value, y_value

    def multiply(self, value: int):
        new_left: List[Variable] = []
        for variable in self.left_side:
            new_variable = Variable(variable.modifier * value, variable.character)
            new_left.append(new_variable)
        
        new_right: List[Variable] = []
        for variable in self.right_side:
            new_variable = Variable(variable.modifier * value, variable.character)
            new_right.append(new_variable)
            
        return Expression(new_left, new_right)
    
    def substitute(self, variable_character: str, variable_value: int):
        new_left = []
        for left_variable in self.left_side:
            if left_variable.character == variable_character:
                value = left_variable.evaluate(variable_value)
                value_variable = Variable(value)
                new_left.append(value_variable)
            else:
                new_variable = Variable(left_variable.modifier, left_variable.character)
                new_left.append(new_variable)
        
        new_right = []
        for right_variable in self.right_side:
            if right_variable.character == variable_character:
                value = right_variable.evaluate(variable_value)
                value_variable = Variable(value)
                new_right.append(value_variable)
            else:
                new_variable = Variable(right_variable.modifier, right_variable.character)
                new_right.append(new_variable)
        
        return Expression(new_left, new_right)
            

class Machine(object):
    def __init__(self, a_increment: Point, b_increment: Point, prize_position: Point):
        self.a_increment = a_increment
        self.b_increment = b_increment
        self.prize_position = prize_position

    def __str__(self) -> str:
        return f"Button A: {self.a_increment}\nButton B: {self.b_increment}\nPrize: {self.prize_position}"

    def calculate_prize_cost(self) -> int:
        x_left_side = [
            Variable(self.a_increment.x,'x'),
            Variable(self.b_increment.x,'y')
        ]
        x_right_side = [
            Variable(self.prize_position.x,)
        ]
        x_expression = Expression(x_left_side, x_right_side)
        
        y_left_side = [
            Variable(self.a_increment.y, 'x'),
            Variable(self.b_increment.y, 'y')
        ]
        y_right_side = [
            Variable(self.prize_position.y)
        ]
        y_expression = Expression(y_left_side, y_right_side)
        
        result = x_expression.combine(y_expression)
        if not result:
            return 0
        
        (x,y) = result
        print(f'Press a {x} times, and press b {y} times')
        return (3 * x) + (1 * y)


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
    x_position = int(line[x_index + 2 : comma_index]) + 10000000000000
    y_position = int(line[y_index:]) + 10000000000000
    return Point(x_position, y_position)


machines: List[Machine] = []
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    while line := in_file.readline():
        a_increment = read_button_increment(line)

        b_line = in_file.readline()
        b_increment = read_button_increment(b_line)

        prize_line = in_file.readline().strip()
        prize_position = read_prize_position(prize_line)

        machine = Machine(a_increment, b_increment, prize_position)
        machines.append(machine)

        empty_line = in_file.readline()

total_prize_cost = 0
for index, machine in enumerate(machines):
    prize_cost = machine.calculate_prize_cost()
    print(f"Machine {index+1} costs {prize_cost}")
    total_prize_cost += prize_cost
    
print(f'Cost to earn each prize: {total_prize_cost}')