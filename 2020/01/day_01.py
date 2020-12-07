from itertools import combinations


def load(data):
    return [int(l) for l in data.strip().split("\n")]


def part1(data):
    numbers = load(data)
    for a, b in combinations(numbers, 2):
        if a + b == 2020:
            return (a * b)


def part2(data):
    numbers = load(data)
    for a, b, c in combinations(numbers, 3):
        if a + b + c == 2020:
            return (a * b * c)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(part1(data))
    print(part2(data))
    
