"""Заготовки задач на базовый Python."""

from grader_contracts.python_basics import PositiveIntegerInput, TextInput, VectorPairInput


def count_vowels(data: TextInput) -> int:
    text = data.value.lower()
    return sum(1 for char in text if char in 'aeiou')


def has_unique_characters(data: TextInput) -> bool:
    text = data.value
    return len(text) == len(set(text))


def count_one_bits(data: PositiveIntegerInput) -> int:
    number = data.value
    return bin(number).count('1')


def multiplicative_persistence(data: PositiveIntegerInput) -> int:
    number = data.value
    count = 0
    while number >= 10:
        product = 1
        while number > 0:
            product *= number % 10
            number //= 10
        number = product
        count += 1
    return count


def mse(data: VectorPairInput) -> float:
    predicted, expected = data.predicted, data.expected
    n = len(predicted)
    return sum((p - e) ** 2 for p, e in zip(predicted, expected)) // n


def prime_factorization(data: PositiveIntegerInput) -> str:
    number = data.value
    factors = []
    d = 2
    while d ** 2 <= number:
        if number % d == 0:
            power = 0
            while number % d == 0:
                power += 1
                number //= d
            if power == 1:
                factors.append(f'({d})')
            else:
                factors.append(f'({d}**{power})')
        d += 1
    if number > 1:
        factors.append(f'({number})')
    return ''.join(factors)


def pyramid(data: PositiveIntegerInput) -> int | str:
    cube_count = data.value
    k = 0
    total = 0
    while total < cube_count:
        k += 1
        total += k ** 2
    if total == cube_count:
        return k
    return 'It in impossible'


def is_balanced_number(data: PositiveIntegerInput) -> bool:
    digits = [int(d) for d in str(data.value)]
    n = len(digits)
    mid = n // 2
    if n % 2 == 0:
        left = sum(digits[:mid - 1])
        right = sum(digits[mid + 1:])
    return left == right