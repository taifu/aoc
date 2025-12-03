from enum import IntEnum
from typing import TypeAlias, Tuple


class Direction(IntEnum):
    RIGHT = 1
    LEFT = -1


Distance: TypeAlias = int
Rotation: TypeAlias = Tuple[Direction, Distance]
Rotations: TypeAlias = Tuple[Rotation, ...]


def load(data: str) -> Rotations:
    return tuple((Direction.RIGHT if line[0] == 'R' else Direction.LEFT, int(line[1:])) for line in data.splitlines())


def count(rotations: Rotations, part: int = 1) -> int:
    pos, pwd = 50, 0
    for direction, distance in rotations:
        for step in range(distance):
            pos = (pos + direction) % 100
            if part == 2 and pos == 0:
                pwd += 1
        if part == 1 and pos == 0:
            pwd += 1
    return pwd


def solve1(data: str) -> int:
    return count(load(data))


def solve2(data: str) -> int:
    return count(load(data), part=2)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
