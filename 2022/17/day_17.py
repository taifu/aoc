from collections import defaultdict


def load(data):
    return [{">": 1, "<": -1}[char] for char in data.strip()]


class Grid:
    def __init__(self, width):
        self.n_rocks = 0
        self.grid = set()
        self.width = width
        self.void = 3j
        self.height = self.void
        self.tops = [-1] * self.width
        self.cache = defaultdict(list)
        self.delta_rocks = self.delta_height = None
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
        print(f"Rocks {self.n_rocks}\n")
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
                print(f"|{line}| {y + 1}")
            if y == 0:
                print(f"+-------+")
                break
            rang = range(min(y - 1, 20), -1, -1)
            print()

    def caching(self, moves):
        key = (self.n_rocks % len(self.rocks), moves, tuple(self.height.imag - t for t in self.tops))
        self.cache[key].append((self.n_rocks, self.height))
        if len(self.cache[key]) > 5:
            delta_rocks = self.cache[key][-1][0] - self.cache[key][-2][0]
            if self.delta_rocks is None:
                self.delta_rocks = delta_rocks
                self.delta_height = self.cache[key][-1][1] - self.cache[key][-2][1]
                assert self.delta_rocks % len(self.rocks) == 0
        return

    def resting(self, moves):
        for xy in self.rock:
            self.grid.add(xy)
            if xy.imag + 4 > self.height.imag:
                self.height = xy + 4j
            if xy.imag > self.tops[int(xy.real)]:
                self.tops[int(xy.real)] = xy.imag
        self.caching(moves)

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
        while True:
            # left/right
            grid.move(self.gases[moves])
            moves = (moves + 1) % len(self.gases)
            # down
            if not grid.move(-1j):
                grid.resting(moves)
                if grid.delta_rocks and delta_height == 0:
                    steps = (n_rocks - grid.n_rocks) // grid.delta_rocks
                    if steps:
                        delta_rocks = steps * grid.delta_rocks
                        delta_height = int(steps * grid.delta_height.imag)
                if grid.n_rocks + delta_rocks == n_rocks:
                    if self.drawing:
                        grid.draw()
                    break
                grid.add_rock()
            if self.drawing:
                grid.draw()
        return int(grid.height.imag) + delta_height - int(grid.void.imag)


def solve1(data, drawing=False):
    return Tetris(load(data), drawing=drawing).height()


def solve2(data):
    return Tetris(load(data)).height(n_rocks=1000000000000)


if __name__ == "__main__":
    import sys
    data = open("input.txt").read()
    print(solve1(data, drawing="-d" in sys.argv))
    print(solve2(data))
