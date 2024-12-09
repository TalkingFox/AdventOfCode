import os, json
from typing import List

input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, 'r') as in_file:
    disk_map = in_file.read().strip()

def to_ascii(value: int)-> str:
    return chr(48 + value)

def from_ascii(value: str) -> int:
    return ord(value) - 48

# disk map uses an alternating indices paradigm
# Every even index (including zero) represents a file. 
#   The file number represents the number of blocks it occupies and its index represents its file id.
# Every odd index represents a length of free-space
def expand_disk_map(disk_map: str) -> List[str]:
    expanded_map: List[str] = []
    for index, character in enumerate(disk_map):
        number_of_blocks = int(character)
        block_character = '.' if (index % 2 == 1) else str(index//2)
        expanded_map.extend([block_character] * number_of_blocks)
    return expanded_map

def compact_expanded_disk_map(expanded_disk_map: List[str]) -> List[str]:
    compacted_disk_map: List[str] = list(expanded_disk_map)
    
    start_cursor = 0
    end_cursor = len(compacted_disk_map)-1
    while start_cursor < end_cursor:
        # move start_cursor to first left-aligned empty block
        while compacted_disk_map[start_cursor] != '.':
            start_cursor += 1
            if start_cursor >= end_cursor:
                return compacted_disk_map
        
        # move end_cursor to first right-aligned populated block
        while compacted_disk_map[end_cursor] == '.':
            end_cursor -= 1
            if start_cursor >= end_cursor:
                return compacted_disk_map
        
        # swap the characters at the cursor positions
        # print(f'start_cursor={start_cursor}, end_cursor={end_cursor}')
        compacted_disk_map[start_cursor],compacted_disk_map[end_cursor] = compacted_disk_map[end_cursor], compacted_disk_map[start_cursor]
    
    return compacted_disk_map

def calculate_checksum(compacted_disk_map: List[str]) -> int:
    checksum = 0
    for index, character in enumerate(compacted_disk_map):
        if character == '.':
            continue
        product = index * int(character)
        checksum += product
    return checksum
    
# print(disk_map)

expanded_disk_map = expand_disk_map(disk_map)
# print(expanded_disk_map)

# with open('expanded_disk.txt', 'w') as out_file:
#     json.dump(expanded_disk_map, out_file)
    
compacted_disk_map = compact_expanded_disk_map(expanded_disk_map)
# print(compacted_disk_map)

# with open('compacted_disk.txt', 'w') as out_file:
#     json.dump(compacted_disk_map, out_file)
checksum = calculate_checksum(compacted_disk_map)
print(checksum)