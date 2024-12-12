from typing import List, Dict, Tuple
import os

input_path = os.path.join(os.path.dirname(__file__), "input.txt")

stones: List[int] = []
with open(input_path, "r") as in_file:
    line = in_file.readline()
    parts = line.split()
    stones = list(map(int, parts))


blink_cache: Dict[int, Tuple[int, int]] = {}


def blink(stone: int) -> List[int]:
    if stone in blink_cache:
        return blink_cache[stone]

    str_stone = str(stone)
    new_stones = []
    if stone == 0:
        new_stones.append(1)
    elif len(str_stone) % 2 == 0:
        midpoint = len(str_stone) // 2
        first_stone = int(str_stone[0:midpoint])
        second_stone = int(str_stone[midpoint:])
        new_stones.append(first_stone)
        new_stones.append(second_stone)
    else:
        new_stones.append(stone * 2024)

    blink_cache[stone] = new_stones
    return new_stones


total_blinks = 40

blink_stone_cache: Dict[int, Dict[int, int]] = {}


def add_to_cache(cache_stone: int, cache_depth: int, cache_value: int):
    if cache_stone not in blink_stone_cache:
        blink_stone_cache[cache_stone] = {}

    blink_stone_cache[cache_stone][cache_depth] = cache_value


def count_blink_stones(stone: int, depth: int, max_depth: int) -> int:
    if stone in blink_stone_cache:
        if depth in blink_stone_cache[stone]:
            return blink_stone_cache[stone][depth]

    blink_stones = blink(stone)
    new_stones = 1 if len(blink_stones) == 2 else 0

    if depth + 1 == max_depth:
        add_to_cache(stone, depth+1, new_stones)
        return new_stones

    for blink_stone in blink_stones:
        blink_count = count_blink_stones(blink_stone, depth + 1, max_depth)
        new_stones += blink_count
    add_to_cache(stone, depth, new_stones)
    return new_stones


stone_count = 0
total_blinks = 75
for stone in stones:
    stone_count += 1
    count = count_blink_stones(stone, 0, total_blinks)
    stone_count += count


print(f"There are {stone_count} stones after {total_blinks } blinks")
