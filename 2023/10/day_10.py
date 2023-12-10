from collections import deque
from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int

    def move(self, inc_x, inc_y):
        return Cell(self.x + inc_x, self.y + inc_y)

    def double(self):
        return Cell(self.x * 2, self.y * 2)


class Maze:
    def __init__(self, data: str):
        self.maze = list(list(line) for line in data.splitlines())
        self.height = len(self.maze)
        self.width = len(self.maze[0])
        self.start = Cell(*self.findstart())

    def findstart(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 'S':
                    return x, y
        raise Exception("S not found")

    def tube(self, cell):
        return self.maze[cell.y][cell.x]

    def is_connected(self, cell1, cell2):
        if abs(cell1.y - cell2.y) == 1 and cell1.x == cell2.x:
            if cell1.y - cell2.y == 1:
                return self.tube(cell1) in ('|', 'L', 'J', 'S') and self.tube(cell2) in ('|', 'F', '7', 'S')
            else:
                return self.tube(cell1) in ('|', 'F', '7', 'S') and self.tube(cell2) in ('|', 'L', 'J', 'S')
        if abs(cell1.x - cell2.x) == 1 and cell1.y == cell2.y:
            if cell1.x - cell2.x == 1:
                return self.tube(cell1) in ('-', '7', 'J', 'S') and self.tube(cell2) in ('-', 'F', 'L', 'S')
            else:
                return self.tube(cell1) in ('-', 'F', 'L', 'S') and self.tube(cell2) in ('-', '7', 'J', 'S')
        return False

    def around(self, cell, double=1):
        for inc_y, inc_x in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_cell = cell.move(inc_x, inc_y)
            if 0 <= next_cell.y < self.height * double and 0 <= next_cell.x < self.width * double:
                yield next_cell

    def loop(self, cell):
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

    def show(self, loop, double=1):
        for y in range(self.height * double):
            row = ''
            for x in range(self.width * double):
                if Cell(x, y) in loop:
                    if double == 2:
                        row += '.'
                    else:
                        row += self.tube(Cell(x, y))
                else:
                    row += ' '
            print(row)

    def flood_fill(self, borders, brick):
        cells = deque(borders)
        filled = []
        seen = []
        while cells:
            cell = cells.popleft()
            if cell not in brick:
                for cell in self.around(cell, double=2):
                    if cell in seen:
                        continue
                    seen.append(cell)
                    if cell not in brick and cell not in filled:
                        filled.append(cell)
                        cells.append(cell)
        return filled

    def inside(self):
        loop = self.loop(self.start)
        double_loop = []
        for cell1, cell2 in zip(loop + [loop[0]], loop[1:] + [loop[0]]):
            cell1 = cell1.double()
            cell2 = cell2.double()
            double_loop.append(cell1)
            double_loop.append(Cell((cell1.x + cell2.x) // 2,
                                    (cell1.y + cell2.y) // 2))
        borders = []
        for y in range(self.height * 2):
            for x in range(self.width * 2):
                if x in (0, self.width * 2 - 1) or y in (0, self.height * 2 - 1):
                    borders.append(Cell(x, y))
        filled = self.flood_fill(borders, double_loop)
        return self.width * self.height - len(loop) - sum(1 for cell in filled if cell.x % 2 == 0 and cell.y % 2 == 0)

    def farthest(self, part2: bool = False) -> int:
        loop = self.loop(self.start)
        return len(loop) // 2


def solve1(data: str) -> int:
    return Maze(data).farthest()


def solve2(data: str) -> int:
    return Maze(data).inside()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
