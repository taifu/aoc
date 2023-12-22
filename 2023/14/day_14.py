class Mirror:
    def __init__(self, raw: str):
        self.map = [list(line) for line in raw.splitlines()]
        self.height, self.width = len(self.map), len(self.map[0])

    def show(self) -> None:
        print()
        for row in self.map:
            print(''.join(row))
        print()

    def tilt(self, direction: tuple[int, int]) -> "Mirror":
        inc_x, inc_y = direction
        # North/South
        if inc_x == 0:
            range_outside = range(self.width)
            range_inside = range(self.height) if inc_y < 0 else range(self.height - 1, -1, -1)
        # East/West
        else:
            range_outside = range(self.height)
            range_inside = range(self.width) if inc_x < 0 else range(self.width - 1, -1, -1)
        for coord1 in range_outside:
            delta = 0
            for coord2 in range_inside:
                x, y = (coord1, coord2) if inc_x == 0 else (coord2, coord1)
                char = self.map[y][x]
                if char == '.':
                    delta += 1
                elif char == '#':
                    delta = 0
                elif char == 'O' and delta:
                    self.map[y - (-inc_y) * delta][x - (-inc_x) * delta] = 'O'
                    self.map[y][x] = '.'
        return self

    def load(self) -> int:
        return sum((self.height - y) if char == 'O' else 0 for y, row in enumerate(self.map) for char in row)

    def cycle(self, cycles: int) -> int:
        cache, loads, n = [], [], 0
        while n < cycles:
            for direction in ((0, -1), (-1, 0), (0, 1), (1, 0)):
                self.tilt(direction)
            key = tuple(''.join(row) for row in self.map)
            loads.append(self.load())
            if key in cache:
                break
            cache.append(key)
            n += 1
        found = cache.index(key)
        return loads[(cycles - found - 1) % (len(cache) - found) + found]


def solve1(data: str) -> int:
    return Mirror(data).tilt((0, -1)).load()


def solve2(data: str) -> int:
    return Mirror(data).cycle(1000000000)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
