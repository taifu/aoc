from collections import defaultdict
from typing import TypeAlias, Callable, Any, Optional
from operator import add, mul
from itertools import combinations


Position: TypeAlias = tuple[int, int]
Operator: TypeAlias = Callable[[Any, Any], Any]


class Map:
    def __init__(self, data: str) -> None:
        self.antennas = defaultdict(list)
        self.occupied = {}
        for y, line in enumerate(data.splitlines()):
            for x, char in enumerate(line):
                if char != '.':
                    self.antennas[char].append((x, y))
                    self.occupied[(x, y)] = char
        self.height, self.width = y + 1, x + 1

    def antinodes(self, xy1: Position, xy2: Position, part2: bool = False) -> list[Position]:
        dx, dy = xy1[0] - xy2[0], xy1[1] - xy2[1]
        ants = []
        while True:
            xy1 = xy1[0] + dx, xy1[1] + dy
            xy2 = xy2[0] - dx, xy2[1] - dy
            new_ants = [ant for ant in (xy1, xy2) if 0 <= ant[0] < self.width and 0 <= ant[1] < self.height]
            if not new_ants:
                break
            ants.extend(new_ants)
            if not part2:
                break
        return ants

    def draw(self, antinodes: set[Position]) -> None:
        print()
        for y in range(self.height):
            line = ""
            for x in range(self.height):
                if (x, y) in self.occupied:
                    line += self.occupied[(x, y)]
                elif (x, y) in antinodes:
                    line += "#"
                else:
                    line += "."
            print(line)
        print()

    def fill_antinodes(self, part2: bool = False) -> int:
        antinodes = set()
        for antenna, positions in self.antennas.items():
            if part2:
                for position in positions:
                    antinodes.add(position)
            for couple in combinations(positions, 2):
                for ant in self.antinodes(*couple, part2):
                    antinodes.add(ant)
        return len(antinodes)

    def count(self) -> int:
        return self.fill_antinodes()

    def count2(self) -> int:
        return self.fill_antinodes(True)


def solve1(data: str) -> int:
    return Map(data).count()


def solve2(data: str) -> int:
    return Map(data).count2()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
