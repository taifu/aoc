raw = open("input.txt").read()

raw_example = """1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2"""


class Point:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        return "P({},{},{},{})".format(self.x, self.y, self.z, self.w)

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) + abs(self.w - other.w)


class Constellation:
    def __init__(self, sun):
        self.points = set()
        self.add(sun)

    def add(self, point):
        self.points.add(point)

    def distance(self, other):
        dist = float("inf")
        for point in self.points:
            new_dist = point.distance(other)
            if new_dist < dist:
                dist = new_dist
        return dist


class Universe:
    def __init__(self, raw, boundary=3):
        self.boundary = boundary
        self._read(raw)
        self._explore()

    def _read(self, raw):
        self.points = []
        for line in raw.strip().split("\n"):
            self.points.append(Point(*[int(p) for p in line.split(",")]))

    def _explore(self):
        self.constellations = []
        points = set(self.points)
        to_create = True
        while points:
            if to_create:
                point = points.pop()
                constellation = Constellation(point)
                self.constellations.append(constellation)
                to_create = False
            while True:
                added = False
                for point in points.copy():
                    if constellation.distance(point) <= self.boundary:
                        constellation.add(point)
                        points.remove(point)
                        added = True
                if not added:
                    to_create = True
                    break


# universe = Universe(raw_example)
# print(len(universe.constellations))

universe = Universe(raw)
print(len(universe.constellations))
