import os
from typing import List

reports: List[List[int]] = []
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    for line in in_file:
        split = list(map(int, line.split()))
        reports.append(split)


# An unsafe report
# 1. Changes direction (goes from increasing to decreasing in values or vice versa)
# 2. or has a value change less than 1 or greater than 3
def is_report_safe(report: List[int]) -> bool:
    last_direction = 0
    is_safe = True
    for index, number in enumerate(report):
        if index == len(report) - 1:
            break

        next_number = report[index + 1]
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

    return is_safe


# Problem dampener - If an unsafe report can be made safe by removing one level, then it is safe.
# Brute force problematic reports by removing levels until either a safe report is found or all levels are examined.
def is_report_one_level_from_safety(report: List[int]) -> bool:
    index = 0
    while index < len(report):
        clone_report = list(report)
        del clone_report[index]

        if is_report_safe(clone_report):
            return True
        index += 1

    return False


safe_reports = 0
for report in reports:
    if is_report_safe(report) or is_report_one_level_from_safety(report):
        safe_reports += 1
        continue

print(f"Considering the problem dampener, there are {safe_reports} safe reports.")
