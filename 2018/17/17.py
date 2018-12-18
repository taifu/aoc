import sys
sys.setrecursionlimit(200000)

raw = open("input.txt").read()

raw_example = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""


SPRING, SAND, CLAY, WATER, FILLED = "+.#|~"
LEFT, DOWN, RIGHT = -1, 0, 1


class Map:
    def __init__(self, raw):
        self.spring_x, self.spring_y = (500, 0)
        self._read(raw)

    def _compile(self, line):
        parts = line.replace(" ", "").split(",")
        line = [0, 0, 0, 0]
        for part in parts:
            coord, value = part.replace(".", " ").split("=")
            d = 0 if coord == 'x' else 2
            if " " in value:
                values = [int(p) for p in value.split()]
            else:
                values = [int(value), int(value)]
            line[d:d + 2] = values
        return line

    def _set_min_max(self, lines):
        self.min_x = self.min_y = float("inf")
        self.max_x = self.max_y = float("-inf")
        for line in lines:
            self.min_x = line[0] if line[0] < self.min_x else self.min_x
            self.min_y = line[2] if line[2] < self.min_y else self.min_y
            self.max_x = line[1] if line[1] > self.max_x else self.max_x
            self.max_y = line[3] if line[3] > self.max_y else self.max_y
        self.min_x -= 1
        self.min_y -= 1
        self.max_x += 2
        self.max_y += 2
        self.width = self.max_x - self.min_x
        self.height = self.max_y - min(self.min_y, 0)

    def _get_point(self, x, y):
        return self._map[y][x - self.min_x]

    def _set_point(self, x, y, char):
        self._map[y][x - self.min_x] = char

    def _set_map(self, lines):
        self._map = [[SAND] * self.width for y in range(self.height)]
        self._set_point(self.spring_x, self.spring_y, SPRING)
        for line in lines:
            for y in range(line[2], line[3] + 1):
                for x in range(line[0], line[1] + 1):
                    self._set_point(x, y, CLAY)

    def _read(self, raw):
        lines = []
        for line in raw.split("\n"):
            if line:
                lines.append(self._compile(line))
        self._set_min_max(lines)
        self._set_map(lines)
        self.spilling = set()
        self.filled = set()

    def draw(self):
        print()
        for y, line in enumerate(self._map):
            new_line = [FILLED if (x + self.min_x, y) in self.filled else
                        (WATER if (x + self.min_x, y) in self.spilling else line[x]) for x in range(len(line))]
            print("".join(new_line))
        print()

    def spill(self):
        self.spilling = set()
        self.filled = set()
        self.fill(self.spring_x, self.spring_y + 1)

    def fill(self, x, y, direction=DOWN):
        self.spilling.add((x, y))

        under = self._get_point(x, y + 1)
        left = self._get_point(x - 1, y)
        right = self._get_point(x + 1, y)

        if not under == CLAY:
            if (x, y + 1) not in self.spilling and 1 <= y + 2 < self.height:
                self.fill(x, y + 1)
            if (x, y + 1) not in self.filled:
                return False

        left_filled = left == CLAY or (x - 1, y) not in self.spilling and self.fill(x - 1, y, -1)
        right_filled = right == CLAY or (x + 1, y) not in self.spilling and self.fill(x + 1, y, 1)

        if direction == DOWN and left_filled and right_filled:
            self.filled.add((x, y))

            dx = x - 1
            while (dx, y) in self.spilling:
                self.filled.add((dx, y))
                dx -= 1

            dx = x + 1
            while (dx, y) in self.spilling:
                self.filled.add((dx, y))
                dx += 1

        return (direction == LEFT and (left_filled or left == CLAY) or
                direction == RIGHT and (right_filled or right == CLAY))

    def first(self):
        tot = 0
        for x, y in self.spilling.union(self.filled):
            if y > self.min_y and y < self.height - 1:
                tot += 1
        return tot

    def second(self):
        return(len(self.filled))


map = Map(raw_example)
map.draw()
map.spill()
map.draw()
print(map.first())
print(map.second())

map = Map(raw)
map.spill()
print(map.first())
print(map.second())
