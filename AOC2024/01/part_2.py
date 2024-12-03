from aoc_input import read_input

first_list, second_list = read_input()
second_list_counts = {}
for number in second_list:
    count = 0
    if number in second_list_counts:
        count = second_list_counts[number]
    second_list_counts[number] = count+1

similarity_sum = 0
for number in first_list:
    multiplier = second_list_counts[number] if number in second_list_counts else 0
    similarity_score = number * multiplier
    similarity_sum += similarity_score

print(f'Similarity Score: {similarity_sum}')