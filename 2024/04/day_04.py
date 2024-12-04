from typing import TypeAlias


Map: TypeAlias = list[list[str]]


def load(data: str) -> Map:
    return [list(line) for line in data.splitlines()]


class XmasMap:
    def __init__(self, data: str) -> None:
        self.map = load(data)
        self.width = len(self.map[0])
        self.height = len(self.map)

    def count(self) -> int:
        total = 0
        for y in range(self.height):
            for x in range(self.width):
                for delta_x in (-1, 0, 1):
                    for delta_y in (-1, 0, 1):
                        if delta_x == delta_y == 0:
                            continue
                        next_x, next_y = x, y
                        for char in 'XMAS':
                            if next_x < 0 or next_x >= self.width or next_y < 0 or next_y >= self.height or self.map[next_y][next_x] != char:
                                break
                            next_x += delta_x
                            next_y += delta_y
                        else:
                            total += 1
        return total

    def count2(self) -> int:
        total = 0
        for y in range(self.height):
            if y < 1 or y >= self.height - 1:
                continue
            for x in range(self.width):
                if x < 1 or x >= self.width - 1 or self.map[y][x] != 'A':
                    continue
                around = (self.map[y - 1][x - 1] + self.map[y - 1][x + 1] + self.map[y + 1][x + 1] + self.map[y + 1][x - 1])
                if around in ('MMSS', 'SMMS', 'SSMM', 'MSSM'):
                    total += 1
        return total


def solve1(data: str) -> int:
    return XmasMap(data).count()


def solve2(data: str) -> int:
    return XmasMap(data).count2()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
