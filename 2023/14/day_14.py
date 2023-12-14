from collections import deque


class Mirror:
    def __init__(self, raw: str):
        self.rocks = {}
        self.rolls = []
        for y, line in enumerate(raw.splitlines()):
            for x, char in enumerate(line):
                if char == '#':
                    self.rocks[complex(x, y)] = True
                if char == 'O':
                    self.rolls.append(complex(x, y))
        self.height, self.width = y + 1, x + 1

    def imag(self, coord):
        return coord.imag

    def real(self, coord):
        return coord.real

    def orders(self, direction):
        if direction.imag != 0:
            getter = self.imag
            limit = self.height
        else:
            getter = self.real
            limit = self.width
        return limit, getter

    def tilt(self, direction):
        limit, getter = self.orders(direction)
        reverse = True if getter(direction) > 0 else False
        new_rolls = set()
        rolls = deque(sorted(self.rolls, key=getter, reverse=reverse))
        while rolls:
            next_roll = rolls.popleft()
            while True:
                next_roll += direction
                if not 0 <= getter(next_roll) < limit or next_roll in self.rocks or next_roll in new_rolls or next_roll in rolls:
                    next_roll -= direction
                    new_rolls.add(next_roll)
                    break
        self.rolls = new_rolls

    def show(self):
        print()
        for y in range(self.height):
            line = ''
            for x in range(self.height):
                if complex(x, y) in self.rocks:
                    line += '#'
                elif complex(x, y) in self.rolls:
                    line += 'O'
                else:
                    line += '.'
            print(line)
        print()

    def load(self, direction):
        self.tilt(direction)
        limit, getter = self.orders(direction)
        return sum(int(limit - getter(roll)) for roll in self.rolls)

    def cycle(self, cycles):
        cache = {}
        n = 0
        limit, getter = self.orders(-1j)
        found = False
        while n < cycles:
            pos = tuple(self.rolls)
            for direction in (-1j, -1, 1j, 1):
                self.tilt(direction)
            new_pos = tuple(self.rolls)
            n += 1
            if pos in cache:
                if not found:
                    length = n - cache[pos][0]
                    n += ((cycles - n) // length) * length
                    found = True
            else:
                cache[pos] = (n, new_pos)
        return sum(int(limit - getter(roll)) for roll in self.rolls)


def solve1(data: str, part2: bool = False) -> int:
    return Mirror(data).load(-1j)


def solve2(data: str) -> int:
    return Mirror(data).cycle(1000000000)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
