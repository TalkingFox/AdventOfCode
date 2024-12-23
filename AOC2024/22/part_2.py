import os
from typing import Dict, List


def mix(value: int, secret: int) -> int:
    return value ^ secret


def prune(secret: int) -> int:
    return secret % 16_777_216


def generate_next_secret(secret: int) -> int:
    product = secret * 64
    secret = mix(product, secret)
    secret = prune(secret)

    quotient = secret // 32
    secret = mix(quotient, secret)
    secret = prune(secret)

    product = secret * 2048
    secret = mix(product, secret)
    secret = prune(secret)
    return secret


def generate_price_sequences(secret: int, iterations: int) -> Dict[str, int]:
    last_price = secret % 10
    prices_by_sequence = {}
    current_sequence: List[int] = []
    for i in range(iterations):
        secret = generate_next_secret(secret)
        price = secret % 10
        change = price - last_price
        if len(current_sequence) == 4:
            current_sequence.pop(0)
            current_sequence.append(change)
            key = str(current_sequence)
            if key not in prices_by_sequence:
                prices_by_sequence[key] = price
        else:
            current_sequence.append(change)
        last_price = price
    return prices_by_sequence


starting_secrets: List[int] = []
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    for line in in_file:
        if line == "\n":
            continue
        secret = int(line)
        starting_secrets.append(secret)


total_sequences: List[str] = []
price_sequences: List[Dict[str, int]] = []
print("Calculating price sequences...")
for index, starting_secret in enumerate(starting_secrets):
    print(f"Secret {index + 1}", end="\r")
    sequence = generate_price_sequences(starting_secret, 2000)
    price_sequences.append(sequence)
    total_sequences.extend(list(sequence.keys()))

print(f"Comparing price sequences. Total Sequences: {len(total_sequences)}")
best_sequence: str = None
best_price: int = 0
for index, sequence in enumerate(total_sequences):
    print(f"Sequence {index + 1}", end='\r')
    price = 0
    for price_sequence in price_sequences:
        if sequence in price_sequence:
            price += price_sequence[sequence]
    if price > best_price:
        best_price = price
        best_sequence = sequence

print(f"{best_sequence} is the best sequence.")
print(f"It provides {best_price} bananas.")
