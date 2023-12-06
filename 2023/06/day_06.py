from math import sqrt, floor, ceil, prod
from dataclasses import dataclass
from typing import TypeAlias, List

Mapping: TypeAlias = List[List[int]]


@dataclass
class Race:
    time: int
    distance: int

    def modes(self) -> int:
        delta_sq = sqrt(self.time**2 - 4 * self.distance)
        x1 = ceil(((-self.time) + delta_sq) / (-2))
        x2 = floor(((-self.time) - delta_sq) / (-2))
        return x2 - x1 + (1 if delta_sq != int(delta_sq) else -1)


class Races:
    def __init__(self, data: str, join: bool = False) -> None:
        lines = [line.split(':')[1].strip() for line in data.splitlines()]
        if join:
            lines = [line.replace(' ', '') for line in lines]
        self.races = [Race(int(p), int(lines[1].split()[n])) for n, p in enumerate(lines[0].split())]

    def total(self) -> int:
        return prod(race.modes() for race in self.races)


def solve1(data: str) -> int:
    return Races(data).total()


def solve2(data: str) -> int:
    return Races(data, join=True).total()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
