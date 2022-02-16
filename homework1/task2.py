def print_sum(n: int) -> int:
    """
    Return sum digits of a number
    """
    return sum(map(int, (num for num in str(n))))


result = print_sum(1234567890)

print(result)
