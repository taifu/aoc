from typing import TypeAlias


Position: TypeAlias = tuple[int, int]


class Map:
    def __init__(self, data: str) -> None:
        self.map = []
        for line in data.splitlines():
            self.map.append(list(line))
            if '^' in line:
                self.start = (line.index('^'), len(self.map) - 1)
                self.map[-1][self.start[0]] = '.'
        self.height, self.width = len(self.map), len(self.map[0])
        self.directions = ((0, -1), (1, 0), (0, 1), (-1, 0))
        self.start_direction = 0

    def draw(self, cell: tuple[int, int]) -> None:
        print()
        for y, xs in enumerate(self.map):
            line = (''.join('o' if (x, y) == cell else c for x, c in enumerate(xs)))
            print(line)
        print()

    def explore(self) -> set[Position]:
        cell = self.start
        direction = self.start_direction
        visited_direction = set()
        while True:
            if (cell, direction) in visited_direction:
                return set()
            visited_direction.add((cell, direction))
            next_cell = (cell[0] + self.directions[direction][0], cell[1] + self.directions[direction][1])
            if not (0 <= next_cell[1] < self.height and 0 <= next_cell[0] < self.width):
                break
            while self.map[next_cell[1]][next_cell[0]] == '#':
                direction = (direction + 1) % len(self.directions)
                next_cell = (cell[0] + self.directions[direction][0], cell[1] + self.directions[direction][1])
            cell = next_cell
        return visited_direction

    def count(self) -> int:
        return len(set(cell for cell, _ in self.explore()))

    def count2(self) -> int:
        possible_obstacle = set(cell for cell, _ in self.explore())
        count = 0
        for obstacle in possible_obstacle:
            self.map[obstacle[1]][obstacle[0]] = '#'
            if not self.explore():
                count += 1
            self.map[obstacle[1]][obstacle[0]] = '.'
        return count


def solve1(data: str) -> int:
    return Map(data).count()


def solve2(data: str) -> int:
    return Map(data).count2()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
