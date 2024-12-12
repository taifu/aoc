from collections import deque
from typing import TypeAlias, List, Tuple, Generator, Set


Plant: TypeAlias = str
Cell: TypeAlias = Tuple[int, int]
Direction: TypeAlias = Tuple[int, int]
Map: TypeAlias = List[List[Plant]]


class Garden:
    def __init__(self, data: str) -> None:
        self.garden: Map = []
        for y, line in enumerate(data.strip().split('\n')):
            self.garden.append([])
            for x, char in enumerate(line):
                self.garden[-1].append(char)
        self.height, self.width = y + 1, x + 1
        self.areas_borders = []
        visited = set()
        for y in range(self.height):
            for x in range(self.height):
                if (x, y) not in visited:
                    visited.add((x, y))
                    region = self.floodfill(x, y, visited)
                    self.areas_borders.append((len(region), self.border(region)))

    def around(self, x: int, y: int) -> Generator[Tuple[Cell, Plant], None, None]:
        for dx, dy in ((1, 0), (-1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                yield (nx, ny), self.garden[ny][nx]

    def floodfill(self, x: int, y: int, visited: Set[Cell]) -> List[Cell]:
        plant = self.garden[y][x]
        area = [(x, y)]
        cells = deque(((x, y), ))
        seen = set()
        while cells:
            x, y = cells.popleft()
            for (x, y), next_plant in self.around(x, y):
                if (x, y) in seen:
                    continue
                seen.add((x, y))
                if (x, y) not in visited:
                    if next_plant == plant:
                        visited.add((x, y))
                        area.append((x, y))
                        cells.append((x, y))
        return area

    def border(self, region: List[Cell]) -> List[Tuple[Cell, Direction]]:
        border = []
        for x, y in region:
            for dx, dy in ((1, 0), (-1, 0), (0, -1), (0, 1)):
                if (x + dx, y + dy) not in region:
                    border.append(((x, y), (dx, dy)))
        return border

    def updown_leftright(self, dx: int, dy: int) -> Tuple[int, int, int, int]:
        if dx == 0:
            return -1, 0, 1, 0
        return 0, -1, 0, 1

    def count_sides(self, border: List[Tuple[Cell, Direction]]) -> int:
        sides = []
        while border:
            (x, y), (dx, dy) = border.pop()
            side = [(x, y, dx, dy)]
            up_left_dx, up_left_dy, down_right_dx, down_right_dy = self.updown_leftright(dx, dy)
            up_left = (x + up_left_dx, y + up_left_dy)
            while (up_left, (dx, dy)) in border:
                border.remove((up_left, (dx, dy)))
                up_left = (up_left[0] + up_left_dx, up_left[1] + up_left_dy)
            down_right = (x + down_right_dx, y + down_right_dy)
            while (down_right, (dx, dy)) in border:
                border.remove((down_right, (dx, dy)))
                down_right = (down_right[0] + down_right_dx, down_right[1] + down_right_dy)
            sides.append(side)
        return len(sides)

    def count(self) -> int:
        return sum(area * len(border) for area, border in self.areas_borders)

    def count2(self) -> int:
        return sum(area * self.count_sides(border) for area, border in self.areas_borders)


garden = None


def solve1(data: str) -> int:
    global garden
    garden = Garden(data)
    return garden.count()


def solve2(data: str) -> int:
    assert garden
    return garden.count2()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
