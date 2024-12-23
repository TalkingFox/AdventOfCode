import os
from typing import List


def mix(value: int, secret: int) -> int:
    return value ^ secret


def prune(secret: int) -> int:
    return secret % 16777216


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


def generate_nth_secret(secret: int, n: int) -> int:
    for i in range(n):
        secret = generate_next_secret(secret)
    return secret


starting_secrets: List[int] = []
input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path, "r") as in_file:
    for line in in_file:
        if line == "\n":
            continue
        secret = int(line)
        starting_secrets.append(secret)


secret_sum = 0
for starting_secret in starting_secrets:
    nth_secret = generate_nth_secret(starting_secret, 2000)
    secret_sum += nth_secret

print(f"Secret sum: {secret_sum}")
