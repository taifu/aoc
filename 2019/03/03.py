class Grid:
    DELTA = {'R': (1, 0),
             'L': (-1, 0),
             'U': (0, 1),
             'D': (0, -1),
             }

    def load(self, wires):
        self.grid = set()
        self.distances = set()
        self.timings = set()
        wires = wires.split("\n")
        assert len(wires) == 2
        timings = {}
        for n_wire, wire in enumerate(wires):
            timing = x = y = 0
            for step in wire.split(","):
                direction, steps = step[0], int(step[1:])
                delta = self.DELTA[direction]
                for n in range(steps):
                    timing += 1
                    x, y = x + delta[0], y + delta[1]
                    if n_wire == 1:
                        if (y, x) in self.grid:
                            self.distances.add(abs(x) + abs(y))
                            self.timings.add(timings[x, y] + timing)
                    elif n_wire == 0:
                        if not (x, y) in timings:
                            timings[x, y] = timing
                        self.grid.add((y, x))


def test_grids():
    g = Grid()
    g.load("""R8,U5,L5,D3
U7,R6,D4,L4""")
    assert min(g.distances) == 6
    assert min(g.timings) == 30
    g.load("""R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83""")
    assert min(g.distances) == 159
    assert min(g.timings) == 610
    g.load("""R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7""")
    assert min(g.distances) == 135
    assert min(g.timings) == 410


if __name__ == "__main__":
    g = Grid()
    g.load(open("input.txt").read().strip())
    print(min(g.distances))
    print(min(g.timings))
