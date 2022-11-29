from itertools import combinations


def load(data):
    return [int(line) for line in data.strip().split("\n")]


def solve1(data):
    increased = 0
    last = None
    numbers = load(data)
    for height in numbers:
        if last is not None:
            if height > last:
                increased += 1
        last = height
    return increased


def solve2(data):
    increased = 0
    a = b = c = None
    numbers = load(data)
    for height in numbers:
        if a is not None:
            if height > a:
                increased += 1
        a = b
        b = c
        c = height
    return increased


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
