def to_snafu(number):
    number5 = ""
    while number:
        remainder = number % 5
        number5 = {2: '2', 1: '1', 0: '0', 3: '=', 4: '-'}[remainder] + number5
        if remainder > 2:
            number += 5
        number = (number - remainder) // 5
    return number5


def from_snafu(number5):
    number, p5 = 0, 1
    for digit in number5[::-1]:
        number += p5 * {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}[digit]
        p5 *= 5
    return number


def solve1(data):
    return to_snafu(sum(from_snafu(number5) for number5 in data.split('\n')))


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
