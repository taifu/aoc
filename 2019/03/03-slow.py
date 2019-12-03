class Grid:
    DELTA = {'R': (1, 0, '-'),
             'L': (-1, 0, '-'),
             'U': (0, 1, '|'),
             'D': (0, -1, '|'),
             }
    INTER = 'X'
    TURN = '+'
    EMPTY = '.'

    def __init__(self, x, y, origin_x=None, origin_y=None):
        self.size_x = x
        self.size_y = y
        self.origin_x = origin_x or x // 2
        self.origin_y = origin_y or y // 2

    def reset(self):
        self.grid = [[self.EMPTY for n in range(self.size_x)] for m in range(self.size_y)]
        self.grid[self.origin_y][self.origin_x] = 'o'

    def show(self):
        for n in range(self.size_y - 1, -1, -1):
            print(''.join(self.grid[n]))

    def load(self, wires):
        self.reset()
        self.distances = set()
        self.timings = set()
        wires = wires.split("\n")
        assert len(wires) == 2
        timings = dict(), dict()
        for n_wire, wire in enumerate(wires):
            timing = 0
            for cycle in range(2):
                x, y = self.origin_x, self.origin_y
                for step in wire.split(","):
                    direction, steps = step[0], int(step[1:])
                    delta = self.DELTA[direction]
                    for n in range(steps):
                        timing += 1
                        if not (x, y) in timings[n_wire]:
                            timings[n_wire][x, y] = timing
                        x, y = x + delta[0], y + delta[1]
                        try:
                            assert x > 0
                            assert y > 0
                            if cycle == 0:
                                if self.grid[y][x] != self.EMPTY:
                                    self.grid[y][x] = self.INTER
                                    self.distances.add(abs(x - self.origin_x) + abs(y - self.origin_y))
                                    self.timings.add(timings[0][x, y] + timing - 1)
                            else:
                                self.grid[y][x] = delta[2]
                        except Exception:
                            print(x, y, self.size_x, self.size_y, self.origin_x, self.origin_y, delta)
                            raise
                    self.grid[y][x] = self.TURN
                if self.grid[y][x] != self.INTER:
                    self.grid[y][x] = delta[2]


def test_grids():
    g = Grid(11, 11, 1, 1)
    g.load("""R8,U5,L5,D3
U7,R6,D4,L4""")
    g.show()
    assert min(g.distances) == 6
    assert min(g.timings) == 30
    g = Grid(1000, 1000)
    g.load("""R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83""")
    g.show()
    assert min(g.distances) == 159
    assert min(g.timings) == 610
    g.load("""R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7""")
    assert min(g.distances) == 135
    assert min(g.timings) == 410


if __name__ == "__main__":
    g = Grid(16000, 15000, 5000, 9999)
    g.load(open("input.txt").read().strip())
    print(min(g.distances))
    print(min(g.timings))
