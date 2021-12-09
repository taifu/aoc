class Floor:
    def __init__(self, data):
        self.map = tuple(tuple(int(c) for c in line) for line in data.strip().split("\n"))
        self.rows = len(self.map)
        self.cols = len(self.map[0])

    def adj(self, x, y):
        adj = []
        for x0, y0 in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if y0 < 0 or y0 >= self.rows or x0 < 0 or x0 >= self.cols:
                continue
            adj.append((self.map[y0][x0], x0, y0))
        return adj

    def low_points(self):
        lows = []
        for y in range(self.rows):
            for x in range(self.cols):
                point = self.map[y][x]
                if point < min(ad[0] for ad in self.adj(x, y)):
                    lows.append((point, x, y))
        return lows

    def explore(self, basin):
        p, x, y = basin[-1]
        for p0, x0, y0 in self.adj(x, y):
            if p0 == 9 or (p0, x0, y0) in basin:
                continue
            if p0 > p:
                basin.append((p0, x0, y0))
                self.explore(basin)
        return basin

    def max_basins(self):
        len_basins = sorted(len(self.explore([(p, x, y)])) for p, x, y in self.low_points())
        return len_basins[-1] * len_basins[-2] * len_basins[-3]


def solve1(data):
    lows = Floor(data).low_points()
    return sum(low[0] for low in lows) + len(lows)


def solve2(data):
    return Floor(data).max_basins()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
