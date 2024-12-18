import os
from typing import List


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
        start_value = pow(8,16)
        record_length = 0
        a_value = start_value
        self.a = a_value
        is_quine_found = False
        program_length = len(self.program)
        while not is_quine_found:
            is_quine_possible = True
            while self.instruction_index < len(self.program):
                instruction = self.program[self.instruction_index]
                operand = self.program[self.instruction_index+1]
                self.__evaluate_instruction__(instruction, operand)
                for output_index in range(len(self.__output__)):
                    if self.__output__[output_index] != self.program[output_index]:
                        is_quine_possible = False
                        break
                if not is_quine_possible:
                    break
                if len(self.__output__) > record_length:
                    record_length = len(self.__output__)
                    print(f'New Record: {a_value} returned output with {len(self.__output__)} matching characters')
            if self.__output__ == self.program:
                is_quine_found = True
            else:
                a_value += 1
                self.a = a_value
                self.__output__ = []
                self.instruction_index = 0
        return a_value

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
print('start state')
machine.print_state()
output = machine.find_quine_for_register_a()
print(f'If Register A == {output}, then the program output will be a quine.')

