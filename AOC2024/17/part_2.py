import os
from typing import Dict, List, Set


class Node(object):
    def __init__(self, input_digit: int, increment: int):
        self.input = input_digit
        self.increment = increment
        self.significant_digits = len(oct(increment))-2

    def make_next(self):
        base_8 = oct(self.input)
        digits_place = len(str(self.increment))
        if base_8[-digits_place] == "7":
            return None
        return Node(self.input + self.increment, self.increment)


class Machine(object):
    def __init__(self, a: int, b: int, c: int, program: List[int]):
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.instruction_index = 0
        self.__output__: List[int] = []

    def evaluate(self) -> List[int]:
        while self.instruction_index < len(self.program):
            instruction = self.program[self.instruction_index]
            operand = self.program[self.instruction_index + 1]
            self.__evaluate_instruction__(instruction, operand)

        return list(self.__output__)

    def find_quine_for_register_a(self) -> int:
        # for each digit in the program (iterating backwards)
        # find all single values (up to 4 digits) that result in the desired digit

        start_digit = pow(8, 15)
        root_node = Node(start_digit, pow(8, 15))

        solved_nodes: List[Node] = []
        queue: List[Node] = [root_node]
        while any(queue):
            node = queue.pop(0)
            output = self.evaluate_for_register_a(node.input)
            if output == self.program:
                return node.input
                solved_nodes.append(node)
                continue

            slice_index = (16 - node.significant_digits) + 1
            if self.program[-slice_index:] == output[-slice_index:]:
                new_node = Node(node.input, pow(8, node.significant_digits - 2))
                queue.insert(0,new_node)
            increment_node = node.make_next()
            if increment_node:
                queue.append(increment_node)

        return solved_nodes

    def evaluate_for_register_a(self, a: int) -> List[int]:
        self.a = a
        self.b = 0
        self.c = 0
        self.__output__ = []
        self.instruction_index = 0
        output = self.evaluate()
        return output

    def __evaluate_instruction__(self, instruction: int, operand: int) -> None:
        should_increment_index = True
        match instruction:
            case 0:
                numerator = self.a
                combo_operand = self.__evaluate_combo_operand__(operand)
                denominator = pow(2, combo_operand)
                self.a = numerator // denominator
            case 1:
                self.b = self.b ^ operand
            case 2:
                combo_operand = self.__evaluate_combo_operand__(operand)
                self.b = combo_operand % 8
            case 3:
                if self.a != 0:
                    should_increment_index = False
                    self.instruction_index = operand
            case 4:
                self.b = self.b ^ self.c
            case 5:
                combo_operand = self.__evaluate_combo_operand__(operand)
                value = combo_operand % 8
                self.__output__.append(value)
            case 6:
                numerator = self.a
                combo_operand = self.__evaluate_combo_operand__(operand)
                denominator = pow(2, combo_operand)
                self.b = numerator // denominator
            case 7:
                numerator = self.a
                combo_operand = self.__evaluate_combo_operand__(operand)
                denominator = pow(2, combo_operand)
                self.c = numerator // denominator

        if should_increment_index:
            self.instruction_index += 2

    def __evaluate_combo_operand__(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise Exception(f"Unsupported operand: {operand}")

    def print_state(self) -> None:
        print(f"Register A: {self.a}")
        print(f"Register B: {self.b}")
        print(f"Register C: {self.c}")
        print(f'Program: {",".join(map(str,program))}')


register_a = 0
register_b = 0
register_c = 0
program: List[str] = []

input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    line = in_file.readline()
    register_a = int(line[12:])

    line = in_file.readline()
    register_b = int(line[12:])

    line = in_file.readline()
    register_c = int(line[12:])

    line = in_file.readline()
    line = in_file.readline().strip()
    program = list(map(int, line[9:].split(",")))

machine = Machine(register_a, register_b, register_c, program)
print("start state")
machine.print_state()
output = machine.find_quine_for_register_a()
print(f"If Register A == {output}, then the program output will be a quine.")
