from typing import Generator
from collections import deque


class Maze:
    def __init__(self, data: str):
        pos = data.index('S')
        self.maze = list(list(line) for line in data.splitlines())
        self.height, self.width = len(self.maze), len(self.maze[0])
        self.start = complex(pos % (self.height + 1), pos // (self.width + 1))

    def tube(self, cell: complex) -> str:
        return self.maze[int(cell.imag)][int(cell.real)]

    def is_connected(self, cell1: complex, cell2: complex) -> bool:
        if abs(cell1.imag - cell2.imag) == 1 and cell1.real == cell2.real:
            if cell1.imag - cell2.imag == 1:
                cell1, cell2 = cell2, cell1
            return self.tube(cell1) in '|F7S' and self.tube(cell2) in '|LJS'
        if abs(cell1.real - cell2.real) == 1 and cell1.imag == cell2.imag:
            if cell1.real - cell2.real == 1:
                cell1, cell2 = cell2, cell1
            return self.tube(cell1) in '-FLS' and self.tube(cell2) in '-7JS'
        return False

    def around(self, cell: complex, factor: int = 1) -> Generator[complex, None, None]:
        for inc_xy in (1j, -1j, 1, -1):
            next_cell = cell + inc_xy
            if 0 <= next_cell.imag < self.height * factor and 0 <= next_cell.real < self.width * factor:
                yield next_cell

    def loop(self, cell: complex) -> list[complex]:
        loop = [cell]
        while True:
            for cell in self.around(loop[-1]):
                if len(loop) > 1 and cell == loop[-2]:
                    continue
                if self.is_connected(loop[-1], cell):
                    loop.append(cell)
                    break
            else:
                raise Exception("Next not found")
            if loop[-1] == self.start:
                return loop[:-1]

    def flood_fill(self, borders: list[complex], wall: set[complex]) -> set[complex]:
        cells = deque(borders)
        seen = set(wall)
        filled = set()
        while cells:
            cell = cells.popleft()
            if cell in wall:
                continue
            for cell in self.around(cell, factor=2):
                if cell in seen:
                    continue
                seen.add(cell)
                if cell not in wall and cell not in filled:
                    filled.add(cell)
                    cells.append(cell)
        return filled

    def inside(self) -> int:
        loop = self.loop(self.start)
        wall = set()
        for cell1, cell2 in zip(loop + [loop[0]], loop[1:] + [loop[0]]):
            cell1 *= 2
            cell2 *= 2
            wall.add(cell1)
            wall.add(complex((cell1.real + cell2.real) // 2,
                             (cell1.imag + cell2.imag) // 2))
        borders = []
        for y in range(self.height * 2):
            for x in range(self.width * 2):
                if x in (0, self.width * 2 - 1) or y in (0, self.height * 2 - 1):
                    cell = complex(x, y)
                    if cell not in wall:
                        borders.append(cell)
        filled = self.flood_fill(borders, wall)
        return (self.width * self.height - len(loop) - sum(
            1 for cell in filled if cell.real % 2 == 0 and cell.imag % 2 == 0))

    def farthest(self, part2: bool = False) -> int:
        return len(self.loop(self.start)) // 2


def solve1(data: str) -> int:
    return Maze(data).farthest()


def solve2(data: str) -> int:
    return Maze(data).inside()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
