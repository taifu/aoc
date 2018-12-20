import math

raw = open("input.txt").read().strip()

raw_example = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"

raw_example_1 = "^ENWWW(NEEE|SSE(EE|N))$"


NORTH, SOUTH, WEST, EAST = list("NSWE")
DELTA = {NORTH: -1j, SOUTH: 1j, WEST: -1, EAST: 1}
INF = 999999999999999


class Map:
    def __init__(self, raw):
        self._read(raw.strip()[1:-1])

    def _explore(self, raw, pos=0j, depth=0):
        if not raw:
            return
        self._visited.add(pos)
        opened = closed = branch = INF
        try:
            opened = raw.index("(")
        except ValueError:
            pass
        try:
            closed = raw.index(")")
        except ValueError:
            pass
        try:
            branch = raw.index("|")
        except ValueError:
            pass
        first = min(branch, opened, closed)
        raw, rest = raw[:first], raw[first + 1:]
        if first < INF:
            if first == branch:
                self._explore(raw, pos, depth)
                raw = self._explore(rest, pos, depth)
            elif first == closed:
                self._explore(raw, pos, depth)
                self._explore(rest, pos, depth)
            elif first == opened:
                self._explore(raw, pos)
                self._explore(rest, pos, depth + 1)
        while raw:
            char, raw = raw[0], raw[1:]
            pos += DELTA[char]
            self._doors.add(pos)
            pos += DELTA[char]
            self._visited.add(pos)
        return

    def _read(self, raw):
        self._visited = set()
        self._doors = set()
        self._explore(raw)
        self._build()

    def _set_point(self, x, y, char):
        self._map[int(y) - self.min_y][int(x) - self.min_x] = char

    def _build(self):
        self.min_x = min(int(p.real) for p in self._visited.union(self._doors))
        self.max_x = max(int(p.real) for p in self._visited.union(self._doors))
        self.min_y = min(int(p.real) for p in self._visited.union(self._doors))
        self.max_y = max(int(p.imag) for p in self._visited.union(self._doors))
        self.width = self.max_x - self.min_x + 1
        self.height = self.max_y - self.min_y + 1
        self._map = [["#"] * self.width for y in range(self.height)]
        for p in self._doors:
            self._set_point(p.real, p.imag, " ")
        for p in self._visited:
            self._set_point(p.real, p.imag, ".")
        self._set_point(0, 0, "X")

    def draw(self):
        print()
        for line in self._map:
            print("".join(line))
        print()

    def furthest(self):
        pass


map = Map(raw_example_1)
map.draw()
print(map.furthest())

map = Map(raw_example)
map.draw()
print(map.furthest())

#map = Map(raw)
print(map.furthest())
