import os, json
from typing import List


class DiskBlock(object):
    def __init__(self, id: str, block_size: int):
        self.id = id
        self.block_size = block_size

    def create_filled(self, id: str, block_size: int) -> List:
        if block_size > self.block_size:
            raise Exception(
                f"Not enough space to fill this block. Requested {block_size}, had: {self.block_size}"
            )
        new_blocks = []
        filled_block = DiskBlock(id, block_size)
        new_blocks.append(filled_block)
        remainder = self.block_size - block_size
        if remainder > 0:
            new_blank = DiskBlock(".", remainder)
            new_blocks.append(new_blank)
        return new_blocks

    def calulate_checksum(self, start_index: int):
        if self.id == ".":
            return 0

        sum = 0
        for index in range(self.block_size):
            product = (start_index + index) * int(self.id)
            sum += product
        return sum


input_path = os.path.join(os.path.dirname(__file__), "input.txt")

disk_blocks = []
with open(input_path, "r") as in_file:
    index = 0
    while char := in_file.read(1):
        if char == "\n":
            index += 1
            continue
        id = "." if index % 2 == 1 else str(index // 2)
        block = DiskBlock(id=id, block_size=int(char))
        disk_blocks.append(block)
        index += 1


def compact_disk_blocks(disk_blocks: List[DiskBlock]) -> List[DiskBlock]:
    compacted_disks: List[DiskBlock] = list(disk_blocks)

    disk_index = len(compacted_disks) - 1
    while disk_index >= 0:
        disk_block = compacted_disks[disk_index]
        if disk_block.id == ".":
            disk_index -= 1
            continue

        if disk_block.id == '5392':
            print('abc')
            
        for free_space_index in range(disk_index):
            free_space_block = compacted_disks[free_space_index]
            if free_space_block.id != ".":
                continue
            if free_space_block.block_size < disk_block.block_size:
                continue
            
            # fill free_space_block
            new_blocks = free_space_block.create_filled(
                disk_block.id, disk_block.block_size
            )
            del compacted_disks[free_space_index]
            disk_index -= 1

            for new_block in reversed(new_blocks):
                compacted_disks.insert(free_space_index, new_block)
                disk_index += 1

            # clear disk_block
            disk_block.id = "."
            break
        # decrement index for next disk evaluation
        disk_index -= 1

    # optional. Smooth out the free_space blocks at the end of the while loop
    return compacted_disks


def calculate_checksum(compacted_disk_map: List[DiskBlock]) -> int:
    checksum = 0

    block_index = 0
    for block in compacted_disk_map:
        checksum += block.calulate_checksum(block_index)
        block_index += block.block_size
    return checksum


def print_blocks(blocks: List[DiskBlock]) -> None:
    output = []
    for block in blocks:
        output.extend([block.id] * block.block_size)
    with open('compacted-part-2.json', 'w') as out_file:
        json.dump(output, out_file)


compacted_disks = compact_disk_blocks(disk_blocks)
print_blocks(compacted_disks)

checksum = calculate_checksum(compacted_disks)
print(checksum)
