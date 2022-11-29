raw_example = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""

raw = open("input.txt").read()


GROUND, TREE, LUMBER = ".", "|", "#"


class Life:
    def __init__(self, raw):
        self.raw = raw

    def _reset(self):
        self.map = []
        for line in self.raw.split("\n"):
            if line:
                self.map.append(list(line))
        self._value = 0
        self.width = len(self.map[0])
        self.height = len(self.map)

    def cell(self, x, y):
        trees = lumbers = grounds = 0
        now = self.map[y][x]
        for dy in range(max(0, y - 1), min(self.height, y + 2)):
            for dx in range(max(0, x - 1), min(self.width, x + 2)):
                if dx != x or dy != y:
                    around = self.map[dy][dx]
                    trees = trees + (1 if around == TREE else 0)
                    grounds = grounds + (1 if around == GROUND else 0)
                    lumbers = lumbers + (1 if around == LUMBER else 0)
        if now == GROUND and trees >= 3:
            return TREE
        if now == TREE and lumbers >= 3:
            return LUMBER
        if now == LUMBER:
            if lumbers >= 1 and trees >= 1:
                return LUMBER
            return GROUND
        return now

    def draw(self):
        print()
        for line in self.map:
            print("".join(line))
        print()

    @property
    def value(self):
        return self._value

    def evolve(self):
        map2 = []
        trees = lumbers = 0
        self._key = ""
        for y in range(self.height):
            map2.append(["."] * self.width)
            for x in range(self.width):
                next_cell = self.cell(x, y)
                if next_cell == TREE:
                    trees += 1
                elif next_cell == LUMBER:
                    lumbers += 1
                map2[y][x] = next_cell
            self._key += "".join(map2[y])
        self._value = trees * lumbers
        self.map = map2

    def go(self, turn, show=False):
        self._reset()
        seen = {}
        values = {}
        if show:
            game.draw()
        for n in range(turn):
            game.evolve()
            values[n] = self._value
            try:
                last = seen[self._key]
                return values[last - 1 + (turn - n) % (n - last)]
            except KeyError:
                seen[self._key] = n
            if show:
                game.draw()
        return(game.value)


# game = Life(raw_example)
# print(game.go(10))

game = Life(raw)
print(game.go(10))

game = Life(raw)
print(game.go(1000000000))

# if seen
# >>> (1000000000 - 1097)
# 999998903
# >>> (1000000000 - 1097) // 28
# 35714246
# >>> (1000000000 - 1097) % 28
# 15

