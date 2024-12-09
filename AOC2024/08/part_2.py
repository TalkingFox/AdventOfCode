import os
from typing import List, Dict


class Vector2(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (
            hasattr(other, "x")
            and hasattr(other, "y")
            and self.x == other.x
            and self.y == other.y
        )

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x},{self.y})"

    def add(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def multiply(self, scalar: int):
        return Vector2(self.x * scalar, self.y * scalar)


class Antenna(object):
    def __init__(self, position: Vector2, id: str):
        self.position = position
        self.id = id


antennae: Dict[str, List[Antenna]] = {}
input_path = os.path.join(os.path.dirname(__file__), "input.txt")

map_width = 0
map_height = 0

with open(input_path, "r") as in_file:
    row = 0
    column = 0
    ends_in_newline = False
    while char := in_file.read(1):
        ends_in_newline = False
        match char:
            case ".":
                pass
            case "\n":
                row += 1
                map_width = column
                column = 0
                ends_in_newline = True
                continue
            case _:
                point = Vector2(column, row)
                antenna = Antenna(point, char)
                if antenna.id not in antennae:
                    antennae[antenna.id] = [antenna]
                else:
                    antennae[antenna.id].append(antenna)
        column += 1
    map_height = row if ends_in_newline else row + 1
    map_width = map_width

print(f"Map Size: height={map_height} width={map_width}")

# generate antinodes by:
# 1. Finding the distance between each like antenna
# 2. Recording all antinodes that distance away from the other node until the map ends.
# 3. And recording all antinodes that distance toward the other node starting two distance units from the source antenna
antinode_positions: List[Vector2] = []
for id, entries in antennae.items():
    for source_index, source_entry in enumerate(entries):
        if source_index == len(entries) - 1:
            continue
        # Only connect antennae to every antenna after it in the list
        # Any antenna before it will already be connected to it
        for target_entry in entries[source_index + 1 :]:
            distance = target_entry.position.subtract(source_entry.position)

            start_antinode = source_entry.position.multiply(1)
            antinode_positions.append(start_antinode)
            
            away_direction = distance.multiply(-1)
            target_antinode_position = source_entry.position.add(away_direction)
            while 0 <= target_antinode_position.x < map_width and 0 <= target_antinode_position.y < map_height:
                antinode_positions.append(target_antinode_position)
                target_antinode_position = target_antinode_position.add(away_direction)
            
            target_antinode_position = source_entry.position.add(distance)
            while 0 <= target_antinode_position.x < map_width and 0 <= target_antinode_position.y < map_height:                
                antinode_positions.append(target_antinode_position)
                target_antinode_position = target_antinode_position.add(distance)
            

print(f"Found {len(antinode_positions)} total antinodes")
# grid: List[List[str]] = []
# for i in range(map_height):
#     row = ['.']  * map_width
#     grid.append(row)

# for position in antinode_positions:
    # print(position)
    # grid[position.y][position.x] = '#'

# print(grid)
        
unique_positions = set(antinode_positions)
print(f'Found {len(unique_positions)} unique antinode positions')
