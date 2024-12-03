import os, re
from typing import List

input_path = os.path.join(os.path.dirname(__file__), "input.txt")

# Regular expression. A match looks like mul(246,14)
# 1. mul - search for the uninterrupted string 'mul'
# 2. \(  - followed by the open parenthetical mark
# 3. \d* - Then a digit of any length
# 4. \,  - Then a comma
# 5. \d* - Then a digit of any length
# 6. \)  - Ending with a close parenthetical mark
expression = r"mul\(\d*\,\d*\)"
with open(input_path, 'r') as in_file:
    contents = in_file.read()
    
    sum = 0
    matches: List[str] = re.findall(expression, contents)
    for match in matches:
        comma_index = match.index(',')
        first_number = int(match[4:comma_index])
        second_number = int(match[comma_index+1:len(match)-1])
        product = first_number * second_number
        sum = sum + product

print(f'The sum of all multiplication instructions is {sum}')