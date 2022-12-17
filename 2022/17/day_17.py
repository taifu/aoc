from collections import defaultdict


def load(data):
    return [{">": 1, "<": -1}[char] for char in data.strip()]


class Grid:
    def __init__(self, width):
        self.n_rocks = 0
        self.grid = set()
        self.width = width
        self.height = 3j
        self.tops = [-1] * self.width
        self.cache = defaultdict(list)
        self.delta = self.delta_height = None
        self.deltas = set()
        self.rocks = [(0, 1, 2, 3),
                      (1, 1j, 1 + 1j, 2 + 1j, 1 + 2j),
                      (0, 1, 2, 2 + 1j, 2 + 2j),
                      (0, 1j, 2j, 3j),
                      (0, 1, 1j, 1 + 1j),
                      ]
        self.add_rock()

    def add_rock(self):
        self.n_rocks += 1
        self.current_pos = 2 + self.height.imag * 1j
        self.rock = tuple(xy + self.current_pos for xy in self.rocks[(self.n_rocks - 1) % len(self.rocks)])

    def draw(self, first=False):
        if first:
            print("\033[2J")
        print("\033[0;0H")
        top = int(self.height.imag) + 2
        rang = range(top, max(-1, top - 20), -1)
        while True:
            for y in rang:
                line = ""
                for x in range(self.width):
                    dot = x + y * 1j
                    if dot in self.grid:
                        line += "#"
                    elif dot in self.rock:
                        line += "@"
                    else:
                        line += "."
                print(f"|{line}| {y}")
            if y == 0:
                print(f"+-------+")
                break
            rang = range(min(y - 1, 20), -1, -1)
            print()

    def caching(self, moves):
        key = (self.n_rocks % len(self.rocks), moves, tuple(self.height.imag - t for t in self.tops))
        self.cache[key].append((self.n_rocks, self.height))
        if len(self.cache[key]) > 5:
            delta = self.cache[key][-1][0] - self.cache[key][-2][0]
            self.deltas.add(delta)
            if self.delta is None:
                self.delta = delta
                self.delta_height = self.cache[key][-1][1] - self.cache[key][-2][1]
                assert self.delta % len(self.rocks) == 0
        return

    def resting(self, moves):
        for xy in self.rock:
            self.grid.add(xy)
            if xy.imag + 4 > self.height.imag:
                self.height = xy + 4j
            if xy.imag > self.tops[int(xy.real)]:
                self.tops[int(xy.real)] = xy.imag
        self.caching(moves)
        self.add_rock()

    def move(self, move):
        next_rock = tuple(xy + move for xy in self.rock)
        for xy in next_rock:
            if xy in self.grid or xy.imag < 0 or xy.real < 0 or xy.real == self.width:
                return False
        self.rock = next_rock
        return True


class Tetris:
    def __init__(self,gases, width=7, drawing=False):
        self.gases = gases
        self.width = width
        self.drawing = drawing

    def height(self, n_rocks=2022):
        grid = Grid(self.width)
        if self.drawing:
            grid.draw(first=True)
        moves = 0
        delta_height = delta_rocks = 0
        while grid.n_rocks + delta_rocks < n_rocks:
            # left/right
            grid.move(self.gases[moves])
            moves = (moves + 1) % len(self.gases)
            # down
            if not grid.move(-1j):
                grid.resting(moves)
                if grid.delta and delta_height == 0:
                    steps = (n_rocks - grid.n_rocks) // grid.delta
                    if steps:
                        delta_rocks = steps * grid.delta
                        delta_height = int(steps * grid.delta_height.imag)
                        pass

            if self.drawing:
                grid.draw()
        return int(grid.height.imag) + delta_height


def solve1(data, drawing=False):
    return Tetris(load(data), drawing=drawing).height()


def solve2(data):
    return Tetris(load(data)).height(n_rocks=1000000000000)
    mostest = []
    for elves, items in load(data).items():
        mostest.append(sum(items))
    return sum(list(reversed(sorted(mostest)))[:3])


if __name__ == "__main__":
    import sys
    data = open("input.txt").read()
    print(solve1(data, drawing="-d" in sys.argv))
    print(solve2(data))
