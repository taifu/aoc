from collections import defaultdict


def load(data):
    grid = {}
    for y, line in enumerate(data.split('\n')):
        for x, char in enumerate(line):
            grid[x + 1j * y] = {'.': 0, '>': 1, '<': -1, '^': -1j, 'v': 1j, '#': None}[char]
    return grid


class Valley:
    def __init__(self, data):
        self.starting_winds = set()
        self.width = self.height = 1
        for xy, wind  in load(data).items():
            self.width = int(max(self.width, xy.real + 1))
            self.height = int(max(self.height, xy.imag + 1))
            if wind not in (None, 0):
                self.starting_winds.add((xy, wind))
        self.enter = 1
        self.exit = self.width - 2 + 1j * (self.height - 1)

    def draw(self, positions, winds, first=False):
        MASK = "\033[{0};1m"
        GREEN = MASK.format("32")
        YELLOW = MASK.format("33")
        CYAN = MASK.format("36")
        if first:
            print("\033[2J")
        print("\033[0;0H\033[0m")
        summed_winds = defaultdict(list)
        for xy, wind in winds:
            summed_winds[xy].append(wind)
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                xy = x + 1j * y
                if xy in positions:
                    line += YELLOW + "E"
                elif xy in (self.enter, self.exit):
                    line += GREEN + "."
                elif xy.real in (0, self.width - 1) or xy.imag in (0, self.height - 1):
                    line += GREEN + "#"
                elif xy not in summed_winds:
                    line += GREEN + "."
                else:
                    xy_winds = summed_winds[xy]
                    if len(xy_winds) > 1:
                        line += str(len(xy_winds))
                    else:
                        line += CYAN + {1: '>', -1: '<', -1j: '^', 1j: 'v'}[xy_winds[0]]
            print(line)
        print()

    def wind_loop(self, winds):
        next_winds = set()
        occupied = set()
        for xy, wind  in winds:
            xy += wind
            if xy.real == 0:
                xy = self.width - 2 + 1j * xy.imag
            elif xy.real == self.width - 1:
                xy = 1 + 1j * xy.imag
            if xy.imag == 0:
                xy = xy.real + 1j * (self.height - 2)
            elif xy.imag == self.height - 1:
                xy = xy.real + 1j
            next_winds.add((xy, wind))
            occupied.add(xy)
        return next_winds, occupied

    def inside(self, pos):
        return (pos.real > 0 and pos.real < self.width - 1 and pos.imag > 0 and pos.imag < self.height - 1)

    def go(self, back_and_forth=False, drawing=False):
        winds = self.starting_winds
        positions = set((self.enter,))
        goals = [self.exit, self.enter, self.exit] if back_and_forth else [self.exit]
        step = 0
        if drawing:
            self.draw(positions, winds, first=True)
        while True:
            winds, occupied = self.wind_loop(winds)
            next_positions = set()
            going_back = False
            for pos in positions:
                for delta_xy in (0, -1, 1, -1j, 1j):
                    next_pos = pos + delta_xy
                    if next_pos == goals[0]:
                        goals.pop(0)
                        if not goals:
                            return step + 1
                        next_positions = set((next_pos,))
                        going_back = True
                        break
                    if (next_pos in (self.exit, self.enter) or self.inside(next_pos)) and not next_pos in occupied:
                        next_positions.add(next_pos)
                if going_back:
                    break
            positions = next_positions
            if drawing:
                self.draw(positions, winds)
            step += 1


def solve1(data, drawing=False):
    return Valley(data).go()


def solve2(data, drawing=False):
    return Valley(data).go(back_and_forth=True, drawing=drawing)


if __name__ == "__main__":
    import sys
    data = open("input.txt").read()
    drawing = '-d' in sys.argv
    print(solve1(data, drawing=drawing))
    print(solve2(data, drawing=drawing))
