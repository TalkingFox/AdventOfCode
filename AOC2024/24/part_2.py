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


x_wires = list(filter(lambda x: x.id.startswith("x"), wires.values()))
x_wires = list(reversed(sorted(x_wires, key=lambda x: x.id)))

y_wires = filter(lambda y: y.id.startswith("y"), wires.values())
y_wires = sorted(y_wires, key=lambda y: y.id)
set_number(y_wires, format(0, f"0{len(y_wires)}b"))

exit()
problematic_x_values = []
for i in range(-1, len(x_wires)):
    string_buffer: List[str] = []
    power_of_2 = 0 if i == -1 else pow(2, i)
    set_number(x_wires, format(power_of_2, f"0{len(x_wires)}b"))
    (x_binary, x_decimal) = get_numbers(reversed(x_wires))
    string_buffer.append(f"X Digit is {x_binary} (base 2) {x_decimal} (base 10)")

    (y_binary, y_decimal) = get_numbers(y_wires)
    string_buffer.append(f"Y Digit is {y_binary} (base 2) {y_decimal} (base 10)")
    expected_sum = x_decimal + y_decimal
    string_buffer.append(
        f"The sum should therefore be {format(expected_sum, f'0{len(x_wires)+1}b')} (base 2) {expected_sum} (base 10)"
    )
    (z_binary, z_decimal) = evaluate_operations(
        operations=source_operations, wires=wires
    )
    string_buffer.append(f"Found sum of {z_binary} (base 2) {z_decimal} (base 10)")
    if z_decimal != expected_sum:
        problematic_x_values.append(power_of_2)
        string_buffer.append(f"This implies a problem at x-value {power_of_2}")
        print("\n".join(string_buffer))
        print()

# swapped_wires: Set[str] = set()
# for i, alpha in enumerate(source_operations):
#     for j, beta in enumerate(source_operations[i+1:]):
#         (alpha.output_id, beta.output_id) = (beta.output_id, alpha.output_id)
        