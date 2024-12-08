import os
from typing import List


class TestEntry(object):
    def __init__(self, test_value: int, operands: List[int]):
        self.test_value = test_value
        self.operands = operands


input_path = os.path.join(os.path.dirname(__file__), "input.txt")
entries: List[TestEntry] = []
with open(input_path, "r") as in_file:
    for line in in_file:
        split = line.split()
        test_value = int(split[0][:-1])
        operands = list(map(int, split[1:]))
        new_entry = TestEntry(test_value, operands)
        entries.append(new_entry)

# Python's built-in solution is itertools.combinations
# I did an alternate approach using base n conversions.
def generate_combinations(elements: List[str], combination_size: int) -> List[List[str]]:
    
    def numberToBase(number: int, base: int, min_padding: int = 1):
        digits = []
        if number == 0:
            while len(digits) < min_padding:
                digits.insert(0,0)
            return digits
        while number:
            digits.append(int(number % base))
            number //= base
        digits = digits[::-1]
        while len(digits) < min_padding:
            digits.insert(0,0)
        return digits
    
    total_combinations = pow(len(elements),combination_size)
    base = len(elements)
    combinations = []
    for i in range(total_combinations):
        combination = numberToBase(i, base, combination_size)
        combinations.append(combination)
    return combinations
        

operators = ['+','*','||']
operator_by_number = {
    0 : '+',
    1 : '*',
    2 : '||'
}
solved_entries: List[TestEntry] = []

total = 0
for entry in entries:
    print(total)
    total += 1
    number_of_operator_patterns = len(entry.operands) - 1
    combinations = generate_combinations(operators, number_of_operator_patterns)
    
    is_entry_solvable = False
    
    # perform a zipper merge of the two lists
    for operator_combination in combinations:
        expression_parts: List[str] = []
        for index in range(len(entry.operands)):
            expression_parts.append(entry.operands[index])
            if index < len(operator_combination):
                operator = operator_by_number[operator_combination[index]]
                expression_parts.append(operator)
        value = expression_parts[0]
        index = 1
        while index < len(expression_parts):
            match expression_parts[index]:
                case '+':
                    value += expression_parts[index+1]
                case '*':
                    value *= expression_parts[index+1]
                case '||':
                    value = int(f'{str(value)}{str(expression_parts[index+1])}')
            index += 2
        
        # debug
        # expression = "".join(map(str,expression_parts))
        # print(f'{expression}={value}')
        if value == entry.test_value:
            # print(f'{entry.test_value} = {expression}')
            solved_entries.append(entry)
            break

print(f'Found {len(solved_entries)} solvable entries')
solve_sum = sum(list(solved_entry.test_value for solved_entry in solved_entries))
print(f'Sum of solvable entries is {solve_sum}')