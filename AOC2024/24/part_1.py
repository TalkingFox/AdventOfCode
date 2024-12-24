import os
from typing import Dict, List


class Wire(object):
    def __init__(self, id: str, value: int):
        self.id = id
        self.value = value


class Operation(object):
    def __init__(self, source_id: str, target_id: str, operator: str, output_id: str):
        self.source_id = source_id
        self.target_id = target_id
        self.operator = operator
        self.output_id = output_id

    def __str__(self) -> str:
        return f"{self.source_id} {self.operator} {self.target_id} -> {self.output_id}"


wires: Dict[str, Wire] = {}
operations: List[Operation] = []

input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    for line in in_file:
        if line == "\n":
            break
        parts = line.split(":")
        wire = Wire(id=parts[0], value=int(parts[1]))
        wires[wire.id] = wire

    for line in in_file:
        if line == "\n":
            break

        line = line.strip()
        parts = line.split(" ")
        operation = Operation(
            source_id=parts[0],
            target_id=parts[2],
            operator=parts[1],
            output_id=parts[4],
        )
        operations.append(operation)

while any(operations):
    i = 0
    while i < len(operations):
        operation = operations[i]
        if operation.source_id not in wires:
            i += 1
            continue
        if operation.target_id not in wires:
            i += 1
            continue

        source_wire = wires[operation.source_id]
        target_wire = wires[operation.target_id]
        result: int = 0
        match operation.operator:
            case "AND":
                result = source_wire.value & target_wire.value
            case "OR":
                result = source_wire.value | target_wire.value
            case "XOR":
                result = source_wire.value ^ target_wire.value
            case _:
                raise Exception(f"Unsupported operator {operation.operator}")
        result_wire = Wire(id=operation.output_id, value=result)
        wires[result_wire.id] = result_wire
        del operations[i]

z_wires = filter(lambda x: x.id.startswith("z"), wires.values())
z_wires = sorted(z_wires, key=lambda x: x.id)
final_number = []
for wire in z_wires:
    final_number.insert(0, wire.value)

binary_number = "".join(map(str, final_number))
decimal_number = int(binary_number, base=2)
print(f"Final number is {binary_number} (Base 2), {decimal_number} (Base 10)")
