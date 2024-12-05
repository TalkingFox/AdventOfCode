import os
from typing import List

input_path = os.path.join(os.path.dirname(__file__), "input.txt")

def is_cross_word(cross_word: str, puzzle: List[str], row: int, column: int) -> bool:
    if row < 1 or row == len(lines) - 1:
        return False
    
    if column < 1 or column == len(lines[row]) - 1:
        return False
    
    left_word: str = "".join(
        [
            puzzle[row-1][column-1],
            puzzle[row][column],
            puzzle[row+1][column+1]
        ]
    )
    right_word: str = "".join(
        [
            puzzle[row-1][column+1],
            puzzle[row][column],
            puzzle[row+1][column-1]
        ]
    )
    
    left_word_matches = left_word == cross_word or left_word[::-1] == cross_word
    right_word_matches = right_word == cross_word or right_word[::-1] == cross_word
    return left_word_matches and right_word_matches

with open(input_path, "r") as in_file:
    lines = in_file.readlines()
    row = 0
    column = 0
    found_crosses = 0
    cross_word = 'MAS'
    for line in lines:
        while column < len(line):
            if line[column] != cross_word[1]:
                column += 1
                continue
            
            if is_cross_word(cross_word, lines, row, column):
                found_crosses += 1
                print(f'{row},{column}')
            column += 1
        row +=1
        column = 0
        
print(f'Found {found_crosses} X-{cross_word}es')
            