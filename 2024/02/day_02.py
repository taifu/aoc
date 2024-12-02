from typing import TypeAlias
from itertools import pairwise


Level: TypeAlias = list[int]
Levels: TypeAlias = list[Level]


def load(data: str) -> Levels:
    return [[int(x) for x in line.split()] for line in data.splitlines()]


def ok(level: Level) -> bool:
    diffs = set([(a - b) for a, b in pairwise(level)])
    return diffs <= set((1, 2, 3)) or diffs <= set((-1, -2, -3))


def count(levels: Levels) -> int:
    return sum(1 if ok(level) else 0 for level in levels)


def count2(levels: Levels) -> int:
    return sum(1 if ok(level) or any(ok(level[:i] + level[i + 1:])
               for i in range(len(level))) else 0 for level in levels)


def solve1(data: str) -> int:
    return count(load(data))


def solve2(data: str) -> int:
    return count2(load(data))


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
