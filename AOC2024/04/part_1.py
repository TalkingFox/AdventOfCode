import os
from typing import List
from enum import Enum


class Direction(Enum):
    NORTH = 1
    NORTHEAST = 2
    EAST = 3
    SOUTHEAST = 4
    SOUTH = 5
    SOUTHWEST = 6
    WEST = 7
    NORTHWEST = 8


def is_word_found(
    word: str, puzzle: List[str], row: int, column: int, direction: Direction
):
    word_length = len(word)

    # upper bounds check
    if direction in {Direction.NORTH, Direction.NORTHEAST, Direction.NORTHWEST}:
        if row < word_length - 1:
            return False

    # eastern bounds check
    if direction in {Direction.EAST, Direction.NORTHEAST, Direction.SOUTHEAST}:
        if column > len(puzzle[column]) - word_length - 1:
            return False

    # lower bounds check
    if direction in {Direction.SOUTH, Direction.SOUTHEAST, Direction.SOUTHWEST}:
        if row > len(puzzle) - word_length:
            return False

    # western bounds check
    if direction in {Direction.WEST, Direction.SOUTHWEST, Direction.NORTHWEST}:
        if column < word_length - 1:
            return False

    row_increment = 0
    column_increment = 0

    match direction:
        case Direction.NORTH:
            row_increment = -1
        case Direction.NORTHEAST:
            row_increment = -1
            column_increment = 1
        case Direction.EAST:
            column_increment = 1
        case Direction.SOUTHEAST:
            row_increment = 1
            column_increment = 1
        case Direction.SOUTH:
            row_increment = 1
        case Direction.SOUTHWEST:
            row_increment = 1
            column_increment = -1
        case Direction.WEST:
            column_increment = -1
        case Direction.NORTHWEST:
            row_increment = -1
            column_increment = -1

    row_index = row
    column_index = column
    counter = 0
    found_word = ""
    while counter < 4:
        found_word += puzzle[row_index][column_index]
        counter += 1
        row_index += row_increment
        column_index += column_increment
    return found_word == word


input_path = os.path.join(os.path.dirname(__file__), "input.txt")

with open(input_path, "r") as in_file:
    lines = in_file.readlines()
    row = 0
    column = 0
    found_words = 0
    word_to_find = "XMAS"
    for line in lines:
        while column < len(line):
            if line[column] != word_to_find[0]:
                column += 1
                continue

            for direction in Direction:
                if is_word_found(word_to_find, lines, row, column, direction):
                    found_words += 1

            column += 1
        row += 1
        column = 0

print(f"Found {word_to_find} {found_words} times.")
