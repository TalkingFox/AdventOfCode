first_list = []
second_list = []
with open('input.txt', 'r') as in_file:
    for index, line in enumerate(in_file):
        split_parts = line.split()
        first_list.append(int(split_parts[0]))
        second_list.append(int(split_parts[1]))

first_list.sort()
second_list.sort()

distance_sum = 0
for index, line in enumerate(first_list):
    pair_distance = abs(first_list[index] - second_list[index])
    distance_sum += pair_distance
    
print(f'Total Distance: {distance_sum}')