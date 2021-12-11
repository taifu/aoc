from collections import deque


class Octopuses:
    def __init__(self, data):
        self.octopuses = list(list(int(x) for x in list(line)) for line in data.strip().split("\n"))
        self.size = len(self.octopuses)

    def flash(self, x, y, flashed, flashing):
        if (x, y) in flashed:
            return
        flashed.add((x, y))
        for y0 in range(max(0, y - 1), min(self.size, y + 2)):
            for x0 in range(max(0, x - 1), min(self.size, x + 2)):
                self.octopuses[y0][x0] = (octopus := self.octopuses[y0][x0] + 1)
                if octopus > 9:
                    if not (x0, y0) in flashed and not (x0, y0) in flashing:
                        flashing.append((x0, y0))

    def loop(self):
        flashed = set()
        flashing = deque()
        for y, line in enumerate(self.octopuses):
            for x, octopus in enumerate(line):
                if (octopus := octopus + 1) > 9:
                    flashing.append((x, y))
                self.octopuses[y][x] = octopus
        while flashing:
            x, y = flashing.pop()
            self.flash(x, y, flashed, flashing)
        for x, y in flashed:
            self.octopuses[y][x] = 0
        return len(flashed)

    def sync(self):
        n = 0
        while True:
            n += 1
            if self.loop() == self.size**2:
                return n


def solve1(data, loop=100):
    octopuses = Octopuses(data)
    return sum(octopuses.loop() for n in range(loop))


def solve2(data):
    return Octopuses(data).sync()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
