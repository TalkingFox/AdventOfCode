import os, re
from typing import List

input_path = os.path.join(os.path.dirname(__file__), "input.txt")

# Regular expression. Match one of "mult(number,number)", "do()", or "dont()"
# 1. Match mult(number,number)
# 1.1 mul - search for the uninterrupted string 'mul'
# 1.2. \(  - followed by the open parenthetical mark
# 1.3. \d* - Then a digit of any length
# 1.4. \,  - Then a comma
# 1.5. \d* - Then a digit of any length
# 1.6. \)  - Ending with a close parenthetical mark
# 2. Match do()
# 2.1 do\(\) - substring search for the characters d, o, (, and ).
# 3. Match dont()
# 3.1 don\'\(\) - substring search for the characters d, o, n, ', (, and ).
expression = r"(mul\(\d*\,\d*\))|(do\(\))|(don\'t\(\))"
with open(input_path, "r") as in_file:
    contents = in_file.read()
    matches = re.findall(expression, contents)
    sum = 0
    enabled = True
    for match in matches:
        mult, should_enable, should_disable = match
        if enabled and mult:
            comma_index = mult.index(",")
            first_number = int(mult[4:comma_index])
            second_number = int(mult[comma_index + 1 : len(mult) - 1])
            product = first_number * second_number
            sum = sum + product

        if enabled and should_disable:
            enabled = False

        if not enabled and should_enable:
            enabled = True

print (f'Considering do and undo commands, the sum of all multiplication instructions is {sum}')