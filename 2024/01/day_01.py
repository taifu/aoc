from typing import TypeAlias


Locations: TypeAlias = tuple[list[int], list[int]]


def load(data: str) -> Locations:
    loc1, loc2 = [], []
    for line in data.splitlines():
        a, b = [int(x) for x in line.split(' ') if x]
        loc1.append(a)
        loc2.append(b)
    return loc1, loc2


def count(locations: Locations) -> int:
    loc1, loc2 = [sorted(loc) for loc in locations]
    diff = 0
    for a, b in zip(loc1, loc2):
        diff += abs(a - b)
    return diff


def count2(locations: Locations) -> int:
    loc1, loc2 = locations
    sim = 0
    for a in loc1:
        sim += a * loc2.count(a)
    return sim


def solve1(data: str) -> int:
    return count(load(data))


def solve2(data: str) -> int:
    return count2(load(data))


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
