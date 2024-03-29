import math


class Cuboid:
    def __init__(self, on, coords):
        self.on = on
        self.coords = tuple(coords)

    @property
    def volume(self):
        return math.prod(((self.coords[n][1] - self.coords[n][0]) for n in range(3)))

    def __sub__(self, cuboid):
        if (overlap := self & cuboid):
            cuboids = []
            for n in range(3):
                if self.coords[n][0] < overlap.coords[n][0]:
                    cuboids.append(Cuboid(True, overlap.coords[:n] + ((self.coords[n][0], overlap.coords[n][0]),) + self.coords[n + 1:]))
                if overlap.coords[n][1] < self.coords[n][1]:
                    cuboids.append(Cuboid(True, overlap.coords[:n] + ((overlap.coords[n][1], self.coords[n][1]),) + self.coords[n + 1:]))
            return cuboids
        else:
            return [self]

    def __and__(self, cuboid):
        all_coords = [(max(cuboid.coords[n][0], self.coords[n][0]), min(cuboid.coords[n][1], self.coords[n][1])) for n in range(3)
                      if cuboid.coords[n][0] < self.coords[n][1] and self.coords[n][0] < cuboid.coords[n][1]]
        if len(all_coords) == 3:
            return Cuboid(self.on, all_coords)
        return None

    def __repr__(self):
        return f"<Cuboid \"{'on' if self.on else 'off'}\" {self.coords}"


class Reactor:
    def __init__(self, data):
        self.cuboids = []
        for line in data.strip().split('\n'):
            parts = line.split(" ")
            self.cuboids.append(Cuboid((parts[0] == 'on'), tuple(tuple((int(p) + n) for n, p in enumerate(part.split('=')[1].split('..'))) for part in parts[1].split(','))))

    def cubes(self, max_coord=None):
        cuboids = []
        for cuboid in self.cuboids:
            cuboids = [sub_cuboid for prev_cuboid in cuboids for sub_cuboid in prev_cuboid - cuboid]
            if cuboid.on:
                cuboids.append(cuboid)
        return sum(cuboid.volume for cuboid in cuboids if max_coord is None or abs(cuboid.coords[0][0]) <= max_coord)


def solve1(data):
    return Reactor(data).cubes(50)


def solve2(data):
    return Reactor(data).cubes()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
