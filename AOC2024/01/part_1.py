from aoc_input import read_input

first_list, second_list = read_input()
first_list.sort()
second_list.sort()

distance_sum = 0
for index, line in enumerate(first_list):
    pair_distance = abs(first_list[index] - second_list[index])
    distance_sum += pair_distance
    
print(f'Total Distance: {distance_sum}')