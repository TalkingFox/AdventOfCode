import os

def read_input():
    first_list = []
    second_list = []
    input_path = os.path.join(os.path.dirname(__file__), 'input.txt')
    print(input_path)
    with open(input_path, 'r') as in_file:
        for index, line in enumerate(in_file):
            split_parts = line.split()
            first_list.append(int(split_parts[0]))
            second_list.append(int(split_parts[1]))
    return first_list, second_list