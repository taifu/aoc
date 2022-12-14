from functools import cmp_to_key


def load(data):
    walls = []
    for line in data.strip().split("\n"):
        walls.append([tuple(int(n) for n in coord.split(",")) for coord in line.split(" -> ")])
    return walls


class Rock:
    def __init__(self, walls, inf=False, paint=False):
        source_x = 500
        self.source = (source_x, 0)
        self.grid = {}
        self.max_xy = [0, 0]
        self.min_xy = [source_x, source_x]
        self.inf = inf
        self.paint = paint
        for wall in walls:
            for xy1, xy2 in zip(wall, wall[1:]):
                assert xy1[0] == xy2[0] or xy1[1] == xy2[1]
                for xy in xy1, xy2:
                    for n, value in enumerate(xy):
                        self.max_xy[n] = max(self.max_xy[n], xy[n])
                        self.min_xy[n] = min(self.min_xy[n], xy[n])
                for y in range(min(xy1[1], xy2[1]), max(xy1[1], xy2[1]) + 1):
                    for x in range(min(xy1[0], xy2[0]), max(xy1[0], xy2[0]) + 1):
                        self.grid[x, y] = "#"
        if self.inf:
            self.max_xy = [source_x*2, self.max_xy[1] + 2]
            self.min_xy[0] = -source_x*2
            for x in range(self.min_xy[0], self.max_xy[0] + 1):
                self.grid[x, self.max_xy[1]] = "#"

    def draw(self):
        print("\033[0;0H")
        for y in range(0, self.max_xy[1] + 1):
            line = ""
            for x in range(self.min_xy[0], self.max_xy[0] + 1):
                line += self.grid.get((x, y), '+' if (x, y) == self.source else '.')
            print(line)

    def fill(self):
        sands = 0
        while True:
            sand = tuple(self.source)
            while True:
                for inc in ((0, 1), (-1, 1), (1, 1)):
                    next_sand = (sand[0] + inc[0], sand[1] + inc[1])
                    if next_sand[0] < self.min_xy[0] or next_sand[0] > self.max_xy[0] or next_sand[1] > self.max_xy[1]:
                        return sands
                    if next_sand not in self.grid:
                        sand = next_sand
                        break
                else:
                    self.grid[sand] = 'o'
                    sands += 1
                    if self.paint:
                        self.draw()
                    if sand == self.source:
                        return sands
                    break


def solve1(data, paint=False):
    return Rock(load(data), paint=paint).fill()


def solve2(data):
    return Rock(load(data), inf=True).fill()


if __name__ == "__main__":
    import sys
    data = open("input.txt").read()
    print(solve1(data, paint=True if '-d' in sys.argv else False))
    print(solve2(data))
