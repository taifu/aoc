from typing import TypeAlias


Levels: TypeAlias = list[list[int]]


def load(data: str) -> Levels:
    return [[int(x) for x in line.split()] for line in data.splitlines()]


def count(levels: Levels) -> int:
    safe = 0
    for level in levels:
        diffs = set([(a - b) for a, b in zip(level, level[1:])])
        if diffs <= set((1, 2, 3)) or diffs <= set((-1, -2, -3)):
            safe += 1
    return safe


def count2(levels: Levels) -> int:
    safe = 0
    for level in levels:
        diffs = set([(a - b) for a, b in zip(level, level[1:])])
        if diffs <= set((1, 2, 3)) or diffs <= set((-1, -2, -3)):
            safe += 1
        else:
            for n in range(len(level)):
                level2 = level[:]
                del level2[n]
                diffs = set([(a - b) for a, b in zip(level2, level2[1:])])
                if diffs <= set((1, 2, 3)) or diffs <= set((-1, -2, -3)):
                    safe += 1
                    break
    return safe


def solve1(data: str) -> int:
    return count(load(data))


def solve2(data: str) -> int:
    return count2(load(data))


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
