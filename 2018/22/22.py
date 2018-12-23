from heapq import heappush, heappop


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


class PointTool:
    def __init__(self, point, tool):
        '''Defines x and y variables'''
        self.point = point
        self.tool = tool

    def __lt__(self, other):
        return self.point.x < other.point.y or self.point.y < other.point.y

    def __eq__(self, other):
        return self.point == other.point and self.tool == other.tool

    def __hash__(self):
        return hash((self.point, self.tool))

    def __repr__(self):
        return "{} {},{}".format(self.tool, self.point.x, self.point.y)


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
        self.width = self.target.x - self.origin.x + 50
        self.height = self.target.y - self.origin.y + 10
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

    def dijkstra(self):
        origin = PointTool(self.origin, TORCH)
        target = PointTool(self.target, TORCH)

        vertices = set([origin, target])
        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)
                if point != origin.point and point != target.point:
                    for tool in self.tool_ok(point):
                        vertices.add(PointTool(point, tool))

        dist = {origin: 0}
        prev = {}
        heapq = [(0, origin)]

        for point in vertices:
            if point != origin:
                dist[point] = float("inf")
            prev[point] = None
            heappush(heapq, (dist[point], point))

        while heapq:
            minutes, current = heappop(heapq)
            tool_ok = self.tool_ok(current.point)
            for p in current.point.around:
                if p.y >= self.height or p.x >= self.width or p == origin.point:
                    continue
                for tool in self.tool_ok(p):
                    if tool in tool_ok:
                        next_minutes = minutes + 1
                        if tool != current.tool:
                            next_minutes += 7
                        next_p = PointTool(p, tool)
                        if next_p not in dist:
                            continue
                        if next_minutes < dist[next_p]:
                            dist[next_p] = next_minutes
                            prev[next_p] = current
                            heappush(heapq, (next_minutes, PointTool(p, tool)))
        return dist[target]


cave = Cave(510, Point(10, 10))
# print(cave.risk)
# print(cave.dijkstra())

# depth: 5616
# target: 10,785
cave = Cave(5616, Point(10, 785))
print(cave.risk)
print(cave.dijkstra())
