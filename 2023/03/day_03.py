from dataclasses import dataclass
from typing import Generator, TypeAlias


Number: TypeAlias = Generator[tuple[int, int, int, int], None, None]
Around: TypeAlias = Generator[tuple[str, int, int], None, None]


@dataclass
class Schema:
    map: list[list[str]]
    height: int
    width: int

    def numbers(self) -> Number:
        for y in range(self.height):
            x = 0
            while x < self.width:
                number = 0
                while self.map[y][x].isdecimal():
                    number = number * 10 + int(self.map[y][x])
                    x += 1
                    if x == self.width:
                        break
                if number:
                    length = len(str(number))
                    yield length, x - length, y, number
                else:
                    x += 1

    def around(self, x: int, y: int, length: int) -> Around:
        for d_y in (-1, 0, 1):
            if 0 <= y + d_y < self.height:
                for d_x in range(-1, length + 1, 1 if d_y != 0 else length + 1):
                    if 0 <= x + d_x < self.width:
                        yield self.map[y + d_y][x + d_x], x + d_x, y + d_y

    def sum(self) -> int:
        tot = 0
        for length, x, y, number in self.numbers():
            if any(cell != "." for cell, dx, dy in self.around(x, y, length)):
                tot += number
        return tot

    def gears(self) -> int:
        tot = 0
        all_numbers = list(self.numbers())
        for n1, (l1, x1, y1, number1) in enumerate(all_numbers[:-1]):
            for l2, x2, y2, number2 in all_numbers[n1 + 1:]:
                if y2 > y1 + 2:
                    break
                if x2 + l2 > x1 - 2 and x2 < x1 + l1 + 2:
                    for cell, dx1, dy1 in self.around(x1, y1, l1):
                        for _, dx2, dy2 in self.around(x2, y2, l2):
                            if dx1 == dx2 and dy1 == dy2 and cell == "*":
                                tot += number1 * number2
        return tot


def load(data: str) -> Schema:
    map = [list(line) for line in data.splitlines()]
    height, width = len(map), len(map[0])
    return Schema(map, height, width)


def solve1(data: str) -> int:
    return load(data).sum()


def solve2(data: str) -> int:
    return load(data).gears()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
