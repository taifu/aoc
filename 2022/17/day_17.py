def load(data):
    return [{">": 1, "<": -1}[char] for char in data.strip()]


class Grid:
    def __init__(self, width):
        self.n_rocks = 0
        self.grid = set()
        self.width = width
        self.current_rock = 0
        self.height = -1j
        self.add_rock()

    def add_rock(self):
        rocks = [(0, 1, 2, 3),
                 (1, 1j, 1 + 1j, 2 + 1j, 1 + 2j),
                 (0, 1, 2, 2 + 1j, 2 + 2j),
                 (0, 1j, 2j, 3j),
                 (0, 1, 1j, 1 + 1j),
                 ]
        self.current_pos = 2 + (self.height.imag + 4) * 1j
        self.rock = tuple(xy + self.current_pos for xy in rocks[self.current_rock % 5])
        self.current_rock += 1
        self.n_rocks += 1

    def draw(self):
        print("\033[0;0H")
        for y in range(int(self.height.imag) + 6, -1, -1):
            line = ""
            for x in range(self.width):
                dot = x + y * 1j
                if dot in self.grid:
                    line += "#"
                elif dot in self.rock:
                    line += "@"
                else:
                    line += "."
            print(f"|{line}|")
        print(f"+-------+")

    def resting(self):
        for xy in self.rock:
            self.grid.add(xy)
            if xy.imag > self.height.imag:
                self.height = xy

    def move(self, move):
        next_rock = tuple(xy + move for xy in self.rock)
        for xy in next_rock:
            if xy in self.grid or xy.imag < 0 or xy.real < 0 or xy.real == self.width:
                return False
        self.rock = next_rock
        return True


class Tetris:
    def __init__(self,gases, width=7):
        self.gases = gases
        self.width = width

    def height(self, n_rocks=2022):
        grid = Grid(self.width)
        #grid.draw()
        moves = 0
        while grid.n_rocks < n_rocks:
            # left/right
            grid.move(self.gases[moves % len(self.gases)])
            moves += 1
            #grid.draw()
            # down
            if not grid.move(-1j):
                grid.resting()
                grid.add_rock()
            #grid.draw()
        return int(grid.height.imag) + 4


def solve1(data):
    return Tetris(load(data)).height()


def solve2(data):
    mostest = []
    for elves, items in load(data).items():
        mostest.append(sum(items))
    return sum(list(reversed(sorted(mostest)))[:3])


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
