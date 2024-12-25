import os
from typing import Dict, Iterable, List, Set, Tuple


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


def get_numbers(wires: Iterable[Wire]) -> Tuple[str, int]:
    number_array = []
    for wire in wires:
        number_array.insert(0, wire.value)
    binary_number = "".join(map(str, number_array))
    decimal_number = int(binary_number, base=2)
    return (binary_number, decimal_number)


def set_number(wires: List[Wire], binary: str) -> None:
    for index, char in enumerate(binary):
        wires[index].value = int(char)


wires: Dict[str, Wire] = {}
source_operations: List[Operation] = []

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
        source_operations.append(operation)


def clone_wires(source_wires: Dict[str, Wire]) -> Dict[str, Wire]:
    new_wires = {}
    for key, wire in source_wires.items():
        new_wires[key] = Wire(id=wire.id, value=wire.value)
    return new_wires


def evaluate_operations(
    wires: Dict[str, Wire], operations: List[Operation]
) -> Tuple[str, int]:
    local_operations = list(operations)
    local_wires = clone_wires(wires)
    while any(local_operations):
        i = 0
        while i < len(local_operations):
            operation = local_operations[i]
            if operation.source_id not in local_wires:
                i += 1
                continue
            if operation.target_id not in local_wires:
                i += 1
                continue

            source_wire = local_wires[operation.source_id]
            target_wire = local_wires[operation.target_id]
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
            local_wires[result_wire.id] = result_wire
            del local_operations[i]

    z_wires = filter(lambda x: x.id.startswith("z"), local_wires.values())
    z_wires = sorted(z_wires, key=lambda x: x.id)
    return get_numbers(z_wires)


num_x_wires = len(list(filter(lambda x: x.id.startswith("x"), wires.values())))
# Useful for visualizing the adder circuits and pattern requisites.
# https://en.wikipedia.org/wiki/Adder_(electronics)#
# find broken gates by applying the following rules
# 1. If the output of a gate is z, then that operation must be a XOR unless is it the final bit, which will be a carry bit AND operation
# 2. If the output of a gate is not z and the inputs are not x and y, then it cannot be XOR.
#       In other words, a XOR operation only occurs when the input is (x,y) or when the output is z.
#       This is because XOR is a summing operation and a sum operations only occur against the source inputs (x,y) and the sum and carry bits (when writing the output).
# 3. Any XOR gate with inputs (x,y) have their output (the sum bit) as one of the inputs to another XOR gate.
#   This is because the sum bit is always XOR'd with the carry bit.
#   This rule does not apply to x00 and y00 because their result is written directly to a z wire.
# 4. Any AND gate must its output correspond to an OR gate (so that carried bits may be counted)
broken_gates: List[Operation] = []
xy_xors_by_output: Dict[str, Operation] = {}
and_gates_by_output: Dict[str, Operation] = {}

for operation in source_operations:
    if (
        operation.output_id.startswith("z")
        and operation.operator != "XOR"
        and operation.output_id != f"z{num_x_wires}"
    ):
        broken_gates.append(operation)
        continue

    if (
        operation.operator == "XOR"
        and not operation.output_id.startswith("z")
        and (
            operation.source_id[0] not in ["x", "y"]
            and operation.target_id[0] not in ["x", "y"]
        )
    ):
        broken_gates.append(operation)
        continue

    if operation.source_id not in ["x00", "y00"] and operation.target_id not in [
        "x00",
        "y00",
    ]:
        if (
            operation.operator == "XOR"
            and operation.target_id[0] in ["x", "y"]
            and operation.source_id[0] in ["x", "y"]
        ):
            xy_xors_by_output[operation.output_id] = operation

        if operation.operator == "AND":
            and_gates_by_output[operation.output_id] = operation

for operation in source_operations:
    if operation.operator == "XOR":
        if operation.source_id in xy_xors_by_output:
            del xy_xors_by_output[operation.source_id]
        if operation.target_id in xy_xors_by_output:
            del xy_xors_by_output[operation.target_id]

    if operation.operator == "OR":
        if operation.source_id in and_gates_by_output:
            del and_gates_by_output[operation.source_id]
        if operation.target_id in and_gates_by_output:
            del and_gates_by_output[operation.target_id]

broken_gates.extend(xy_xors_by_output.values())
broken_gates.extend(and_gates_by_output.values())

print(f"Found {len(broken_gates)} broken gates.")
outputs = ",".join(sorted(map(lambda x: x.output_id, broken_gates)))
print(outputs)
