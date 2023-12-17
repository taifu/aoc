from typing import Generator
from collections import defaultdict
from heapq import heappop, heappush


class Map:
    def __init__(self, raw: str, min_steps: int = 1, max_steps: int = 3):
        self.map = [[int(c) for c in line] for line in raw.splitlines()]
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.dxy = ((0, 1), (1, 0), (0, -1), (-1, 0))
        self.graph = defaultdict(list)
        for y in range(self.height):
            for x in range(self.height):
                for (nx, ny, direction, heat) in self.next(x, y, min_steps, max_steps):
                    self.graph[(x, y)].append((heat, nx, ny, direction))

    def heatloss(self) -> int:
        #  dijkstra
        visited = set()
        min_heat: dict[tuple[int, int, int], int] = {}
        queue: list[tuple[int, int, int, int]] = [(0, 0, 0, -1)]
        while queue:
            heat, x, y, direction = heappop(queue)
            if (x, y) == (self.width - 1, self.height - 1):
                return heat
            if (x, y, direction) in visited:
                continue
            visited.add((x, y, direction))
            for plus_heat, nx, ny, next_direction in self.graph.get((x, y), ()):
                if (nx, ny, next_direction) in visited:
                    continue
                if direction != -1 and next_direction % 2 == direction % 2:
                    continue
                prev_heat = min_heat.get((nx, ny, next_direction), float("inf"))
                next_heat = heat + plus_heat
                if next_heat < prev_heat:
                    min_heat[(x, y, next_direction)] = next_heat
                    heappush(queue, (next_heat, nx, ny, next_direction))
        raise Exception("Not found")

    def inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def next(self, x: int, y: int, min_steps: int, max_steps: int) -> Generator[tuple[int, int, int, int], None, None]:
        for direction, (dx, dy) in enumerate(self.dxy):
            for steps in range(min_steps, max_steps + 1):
                if dx:
                    nx = x + dx * steps
                    if self.inside(nx, y):
                        yield nx, y, direction, sum(self.map[y][px] for px in range(x + dx, nx + dx, dx))
                if dy:
                    ny = y + dy * steps
                    if self.inside(x, ny):
                        yield x, ny, direction, sum(self.map[py][x] for py in range(y + dy, ny + dy, dy))


def solve1(data: str) -> int:
    return Map(data).heatloss()


def solve2(data: str) -> int:
    return Map(data, 4, 10).heatloss()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
