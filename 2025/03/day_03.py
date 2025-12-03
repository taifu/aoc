from typing import TypeAlias, Generator, Tuple  # noqa: F401


Battery: TypeAlias = Tuple[int, ...]
Batteries: TypeAlias = Tuple[Battery, ...]


def load(data: str) -> Batteries:
    return tuple(tuple(int(c) for c in line) for line in data.strip().splitlines())


def count(batteries: Batteries, length: int = 2) -> int:
    tot = 0
    for battery in batteries:
        maxs, punt = [], 0
        for cont in range(length - 1, 0, -1):
            maxs.append(max(battery[punt:-cont]))
            punt = battery.index(maxs[-1], punt) + 1
        tot += int("".join(str(m) for m in maxs + [max(battery[punt:])]))
    return tot


def solve1(data: str) -> int:
    return count(load(data))


def solve2(data: str) -> int:
    return count(load(data), 12)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
