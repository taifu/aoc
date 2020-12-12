from itertools import combinations


def load(data):
    return [int(line) for line in data.strip().split("\n")]


def solve(data):
    numbers = load(data)
    for a, b in combinations(numbers, 2):
        if a + b == 2020:
            return (a * b)


def solve2(data):
    numbers = load(data)
    for a, b, c in combinations(numbers, 3):
        if a + b + c == 2020:
            return (a * b * c)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve2(data))
