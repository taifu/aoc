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
        self._read(raw)

    def _read(self, raw):
        self.map = []
        for line in raw.split("\n"):
            if line:
                self.map.append(list(line))
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
        trees = lumbers = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == TREE:
                    trees += 1
                elif self.map[y][x] == LUMBER:
                    lumbers += 1
        return trees * lumbers

    def evolve(self):
        map2 = []
        for y in range(self.height):
            map2.append(["."] * self.width)
            for x in range(self.width):
                map2[y][x] = self.cell(x, y)
        self.map = map2


game = Life(raw_example)
game.draw()
for n in range(10):
    game.evolve()
game.draw()
print(game.value)

game = Life(raw)
game.draw()
for n in range(10000000):
    game.evolve()
    if n > 100:
        print(n + 1, game.value)
game.draw()
print(game.value)

if seen
>>> (1000000000 - 1097)
999998903
>>> (1000000000 - 1097) // 28
35714246
>>> (1000000000 - 1097) % 28
15

