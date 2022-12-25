def to_snafu(number):
    number5 = ""
    while number:
        remainder = number % 5
        number5 = ['0', '1', '2', '=', '-'][remainder] + number5
        number = (number - remainder + (5 if remainder > 2 else 0)) // 5
    return number5


def from_snafu(number5):
    return sum(5**n * ({'-': -1, '=': -2}.get(digit) or int(digit)) for n, digit in enumerate(number5[::-1]))


def solve1(data):
    return to_snafu(sum(map(from_snafu, data.split('\n'))))


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
