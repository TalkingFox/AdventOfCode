import os
from typing import List

input_path = os.path.join(os.path.dirname(__file__), "input.txt")

stones: List[int] = []
with open(input_path, "r") as in_file:
    line = in_file.readline()
    parts = line.split()
    stones = list(map(int, parts))


def blink(stones: List[int]) -> List[int]:
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
            continue
        
        str_stone = str(stone)
        if len(str_stone) % 2 == 0:
            midpoint = len(str_stone)//2
            first_stone = int(str_stone[0:midpoint])
            second_stone = int(str_stone[midpoint:])
            new_stones.append(first_stone)
            new_stones.append(second_stone)
            continue
        
        new_stones.append(stone * 2024)
    return new_stones

total_blinks = 25
blink_stones = stones
for index in range(total_blinks):
    blink_stones = blink(blink_stones)
    print(f'There are {len(blink_stones)} stones after {index + 1 } blinks')    