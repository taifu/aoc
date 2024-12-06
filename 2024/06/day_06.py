class Map:
    def __init__(self, data: str) -> None:
        self.map = []
        for line in data.splitlines():
            self.map.append(list(line))
            if '^' in line:
                self.start = complex(line.index('^'), len(self.map) - 1)
                self.map[-1][int(self.start.imag)] = '.'
        self.height, self.width = len(self.map), len(self.map[0])
        self.direction = -1j
        self.directions = [-1j, 1, 1j, -1, -1j]

    def draw(self, cell: complex) -> None:
        print()
        for y, xs in enumerate(self.map):
            line = (''.join('o' if y == cell.imag and x == cell.real else c for x, c in enumerate(xs)))
            print(line)
        print()

    def explore(self, cell: complex, direction: complex) -> set[complex]:
        visited = set()
        visited_direction = set()
        while True:
            visited.add(cell)
            if (cell, direction) in visited_direction:
                return set()
            visited_direction.add((cell, direction))
            next_cell = cell + direction
            if not (0 <= next_cell.imag < self.height and 0 <= next_cell.real < self.width):
                break
            while self.map[int(next_cell.imag)][int(next_cell.real)] == '#':
                direction = self.directions[self.directions.index(direction) + 1]
                next_cell = cell + direction
            cell = next_cell
        return visited

    def count(self) -> int:
        return len(self.explore(self.start, self.direction))

    def count2(self) -> int:
        possible_obstacle = self.explore(self.start, self.direction)
        count = 0
        for obstacle in possible_obstacle:
            self.map[int(obstacle.imag)][int(obstacle.real)] = '#'
            if not self.explore(self.start, self.direction):
                count += 1
            self.map[int(obstacle.imag)][int(obstacle.real)] = '.'
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
