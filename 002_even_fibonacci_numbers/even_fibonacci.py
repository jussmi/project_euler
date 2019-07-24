def fibonacci(limit: int):
    """Function that yields the next fibonacci numbers in the sequence."""
    current_number, next_number = 0, 1
    while current_number <= limit:
        current_number, next_number = next_number, current_number+next_number
        yield current_number

def main(limit_num: int) -> int:
    fib_seq = fibonacci(limit_num)

    return sum([num for num in fib_seq if num % 2 == 0])

if __name__ == '__main__':
    print(main(4_000_000))
