from collections import deque

raw = open("input.txt").read().strip()

raw_example = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"

raw_example_1 = "^ENWWW(NEEE|SSE(EE|N))$"


NORTH, SOUTH, WEST, EAST = list("NSWE")
DELTA = {NORTH: -1j, SOUTH: 1j, WEST: -1, EAST: 1}
INF = 999999999999999


class Map:
    def __init__(self, raw):
        self._read(raw.strip()[1:-1])

    def _explore(self, raw, pos=0j):
        if not raw:
            return
        self._visited.add(pos)
        start_pos = pos
        while raw:
            char, raw = raw[0], raw[1:]
            if char == "(":
                raw = self._explore(raw, pos)
            elif char == ")":
                return raw
            elif char == "|":
                pos = start_pos
                continue
            else:
                delta = DELTA[char]
                pos += delta
                self._visited.add(pos)
                if delta.imag != 0:
                    self._doors_h.add(pos)
                else:
                    self._doors_v.add(pos)
                pos += delta
                self._visited.add(pos)
        return

    def _read(self, raw):
        self._visited = set()
        self._doors_v = set()
        self._doors_h = set()
        self._explore(raw)
        self._build()

    def _set_point(self, xy, char):
        self._map[int(xy.imag) - self.min_y][int(xy.real) - self.min_x] = char

    def _get_point(self, xy):
        return self._map[int(xy.imag) - self.min_y][int(xy.real) - self.min_x]

    def _build(self):
        self.min_x = min(int(p.real) for p in self._visited) - 1
        self.max_x = max(int(p.real) for p in self._visited) + 1
        self.min_y = min(int(p.real) for p in self._visited) - 1
        self.max_y = max(int(p.imag) for p in self._visited) + 1
        self.width = self.max_x - self.min_x + 1
        self.height = self.max_y - self.min_y + 1
        self._map = [["#"] * self.width for y in range(self.height)]
        for p in self._visited:
            self._set_point(p, ".")
        for p in self._doors_v:
            self._set_point(p, "|")
        for p in self._doors_h:
            self._set_point(p, "-")
        self._set_point(0j, "X")

    def draw(self):
        print()
        for line in self._map:
            print("".join(line))
        print()

    def longest(self):
        visited = set()
        max_doors = 0
        thousand_doors = set()
        paths = deque([(0j, 0)])
        while paths:
            pos, doors = paths.popleft()
            if pos in visited:
                continue
            visited.add(pos)
            if doors > max_doors:
                max_doors = doors
            if doors >= 1000:
                thousand_doors.add(pos)
            for direction, delta in DELTA.items():
                char = self._get_point(pos + delta)
                if char in ("|-"):
                    paths.append((pos + delta * 2, doors + 1))
        return max_doors, len(thousand_doors)


map = Map(raw)
a, b = map.longest()

print(a)
print(b)
