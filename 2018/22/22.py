class Point:
    def __init__(self, x, y):
        '''Defines x and y variables'''
        self.x = x
        self.y = y

    def __repr__(self):
        return "{},{}".format(self.x, self.y)

    @property
    def left(self):
        return Point(self.x - 1, self.y)

    @property
    def above(self):
        return Point(self.x, self.y - 1)

    @property
    def below(self):
        return Point(self.x, self.y + 1)

    @property
    def right(self):
        return Point(self.x + 1, self.y)

    @property
    def ok(self):
        return self.x >= 0 and self.y >= 0

    @property
    def around(self):
        return [p for p in (self.above, self.right, self.left, self.below) if p.ok]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


ROCKY = '.'
WET = '='
NARROW = '|'
NEITHER, TORCH, CLIMBING = "N", "T", "C"


class Cave:
    def __init__(self, depth, target):
        self.origin = Point(0, 0)
        self.depth = depth
        self.target = target
        self._build()

    def _build(self):
        self.width = self.target.x - self.origin.x + 500
        self.height = self.target.y - self.origin.y + 500
        erosions = {}
        self.risk = 0
        self._map = {}
        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)
                if point not in erosions:
                    if point == self.target:
                        geo_index = 0
                    elif point.y == 0:
                        geo_index = point.x * 16807
                    elif point.x == 0:
                        geo_index = point.y * 48271
                    else:
                        geo_index = erosions[point.left] * erosions[point.above]
                    erosions[point] = (geo_index + self.depth) % 20183
                    type = NARROW if erosions[point] % 3 == 2 else WET if erosions[point] % 3 == 1 else ROCKY
                    if y <= self.target.y and x <= self.target.x:
                        self.risk += 1 if type == WET else 2 if type == NARROW else 0
                    self._map[point] = type

    def draw(self):
        print()
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                point = Point(x, y)
                line += "M" if point == self.origin else "T" if point == self.target else self._map[Point(x, y)]
            print(line)
        print()

    def tool_ok(self, point):
        if point == self.target:
            return [TORCH]
        type = self._map[point]
        if type == WET:
            return NEITHER, CLIMBING
        elif type == NARROW:
            return NEITHER, TORCH
        return TORCH, CLIMBING

    def best_around(self, point):
        best, tools = self._best[point]
        bested = set()
        for tool in tools:
            for p in point.around:
                if p.y >= self.height or p.x >= self.width:
                    continue
                tools_ok = self.tool_ok(p)
                if tool in tools_ok:
                    next_best = best + 1
                    next_tools = [tool]
                else:
                    next_best = best + 8
                    next_tools = tools_ok
                for p_tool in next_tools:
                    if p not in self._best or self._best[p][0] > next_best:
                        self._best[p] = (next_best, [p_tool])
                        if p.y < point.y or p.x < point.x:
                            self.best_around(p)
                    elif self._best[p][0] == next_best and p_tool not in self._best[p][1]:
                        self._best[p][1].append(p_tool)
                        if p.y < point.y or p.x < point.x:
                            self.best_around(p)
        return bested

    def explore(self):
        self._best = {self.origin: (0, [TORCH])}
        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)
                self.best_around(point)
        return self._best[self.target]


"""
1  function Dijkstra(Graph, source):
2      dist[source] ← 0                           // Initialization
3
4      create vertex set Q
5
6      for each vertex v in Graph:
7          if v ≠ source
8              dist[v] ← INFINITY                 // Unknown distance from source to v
9          prev[v] ← UNDEFINED                    // Predecessor of v
10
11         Q.add_with_priority(v, dist[v])
12
13
14     while Q is not empty:                      // The main loop
15         u ← Q.extract_min()                    // Remove and return best vertex
16         for each neighbor v of u:              // only v that are still in Q
17             alt ← dist[u] + length(u, v)
18             if alt < dist[v]
19                 dist[v] ← alt
20                 prev[v] ← u
21                 Q.decrease_priority(v, alt)
22
23     return dist, prev
"""


cave = Cave(510, Point(10, 10))
print(cave.risk)
print(cave.explore())

# depth: 5616
# target: 10,785
cave = Cave(5616, Point(10, 785))
print(cave.risk)
print(cave.explore())
#1062
