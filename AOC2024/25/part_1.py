import os
from typing import List, Tuple


class Lock(object):
    def __init__(self, grid: List[str]) -> None:
        self.__max_height__ = len(grid) - 2
        # initialize to 7 in the event that a pin extends to the top
        # should never happen.
        self.heights: List[int] = [self.__max_height__] * 5
        remaining_columns = [0, 1, 2, 3, 4]
        for row_index, row in enumerate(grid):
            i = 0
            while i < len(remaining_columns):
                column = remaining_columns[i]
                if row[column] == ".":
                    self.heights[column] = row_index - 1
                    del remaining_columns[i]
                else:
                    i += 1

    def __str__(self) -> str:
        return ",".join(list(map(str, self.heights)))


class Key(object):
    def __init__(self, grid: List[str]) -> None:
        self.__max_height__ = len(grid) - 2
        # initialize to 7 in the event that a pin extends to the bottom
        # should never happen.
        self.heights: List[int] = [len(grid)] * 5
        remaining_columns = [0, 1, 2, 3, 4]
        for row_index, row in enumerate(grid):
            i = 0
            while i < len(remaining_columns):
                column = remaining_columns[i]
                if row[column] == "#":
                    self.heights[column] = (self.__max_height__) - (row_index - 1)
                    del remaining_columns[i]
                else:
                    i += 1

    def __str__(self) -> str:
        return ",".join(list(map(str, self.heights)))

    def fits_lock(self, lock: Lock) -> bool:
        for i in range(len(self.heights)):
            maximum_lock_height = self.__max_height__ - self.heights[i]
            if maximum_lock_height < lock.heights[i]:
                return False
        return True


locks: List[Lock] = []
keys: List[Key] = []
input_path = os.path.join(os.path.dirname(__file__), "input.txt")


def parse_grid(grid: List[str]) -> None:
    if grid[0][0] == ".":
        key = Key(grid)
        keys.append(key)
    else:
        lock = Lock(grid)
        locks.append(lock)


with open(input_path, "r") as in_file:
    active_grid: List[str] = []
    for line in in_file:
        line = line.strip()
        if not line:
            parse_grid(active_grid)
            active_grid = []
        else:
            active_grid.append(line)
    if len(active_grid) > 0:
        parse_grid(active_grid)

keys_and_locks: List[Tuple[Key, Lock]] = []
for key in keys:
    for lock in locks:
        if key.fits_lock(lock):
            keys_and_locks.append((key, lock))

print(f"Found {len(keys_and_locks)} unique key/lock combinations.")
