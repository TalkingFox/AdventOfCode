import math, os

reports = []
input_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(input_path, 'r') as in_file:
    for line in in_file:
        split = list(map(int, line.split()))
        reports.append(split)
        

safe_reports = 0
for report in reports:
    # An unsafe report 
    # 1. Changes direction (goes from increasing to decreasing in values or vice versa) 
    # 2. or has a value change less than 1 or greater than 3
    last_direction = 0
    is_safe = True
    for index, number in enumerate(report):
        if index == len(report)-1:
            break
        
        next_number = report[index+1]
        difference = number - next_number
        abs_difference = abs(difference)
        if abs_difference < 1 or abs_difference > 3:
            is_safe = False
            break
        
        direction = 1 if difference > 0 else -1
        if last_direction == 0:
            last_direction = direction
            continue
            
        if last_direction != direction:
            is_safe = False
            break
        
    if is_safe:
        safe_reports+=1


print(f'There are {safe_reports} safe reports.')