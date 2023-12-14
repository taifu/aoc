from collections import deque


class Mirror:
    def __init__(self, raw: str):
        self.map = [list(line) for line in raw.splitlines()]
        self.height, self.width = len(self.map), len(self.map[0])

    def orders(self, direction):
        if direction.imag != 0:
            getter = self.imag
            limit = self.height
        else:
            getter = self.real
            limit = self.width
        return limit, getter

    def show(self):
        print()
        for row in self.map:
            print(''.join(row))
        print()

    def tilt(self, direction):
        inc_x, inc_y = direction
        # North/South
        if inc_x == 0:
            range_x = range(self.width)
            range_y = range(self.height) if inc_y < 0 else range(self.height - 1, -1, -1)
            for x in range_x:
                delta = 0
                for y in range_y:
                    char = self.map[y][x]
                    if char == '.':
                        delta += 1
                    elif char == '#':
                        delta = 0
                    elif char == 'O' and delta:
                        self.map[y - (-inc_y) * delta][x] = 'O'
                        self.map[y][x] = '.'
        # East/West
        else:
            range_x = range(self.width) if inc_x < 0 else range(self.width - 1, -1, -1)
            range_y = range(self.height)
            for y in range_y:
                delta = 0
                for x in range_x:
                    char = self.map[y][x]
                    if char == '.':
                        delta += 1
                    elif char == '#':
                        delta = 0
                    elif char == 'O' and delta:
                        self.map[y][x - (-inc_x) * delta] = 'O'
                        self.map[y][x] = '.'
        return self

    def load(self):
        return sum((self.height - y) if char == 'O' else 0 for y, row in enumerate(self.map) for char in row)

    def cycle(self, cycles):
        cache = []
        loads = []
        n = 0
        while n < cycles:
            for direction in ((0, -1), (-1, 0), (0, 1), (1, 0)):
                self.tilt(direction)
            key = tuple(''.join(row) for row in self.map)
            loads.append(self.load())
            if key in cache:
                break
            n += 1
            cache.append(key)
        found = cache.index(key) + 1
        return loads[(cycles - found) % (len(cache) - found + 1) + found - 1]


def solve1(data: str, part2: bool = False) -> int:
    return Mirror(data).tilt((0, -1)).load()


def solve2(data: str) -> int:
    return Mirror(data).cycle(1000000000)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
