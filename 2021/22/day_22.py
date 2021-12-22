import math


class Cuboid:
    def __init__(self, on, coords):
        self.on = on
        self.coords = tuple(coords)

    @property
    def volume(self):
        return math.prod(((self.coords[n][1] - self.coords[n][0]) for n in range(3)))

    def subtract(self, cuboid):
        if (overlap := self.overlap(cuboid)):
            cuboids = []
            if self.coords[0][0] < overlap.coords[0][0]:
                cuboids.append(Cuboid(True, ((self.coords[0][0], overlap.coords[0][0]), self.coords[1], self.coords[2])))
            if overlap.coords[0][1] < self.coords[0][1]:
                cuboids.append(Cuboid(True, ((overlap.coords[0][1], self.coords[0][1]), self.coords[1], self.coords[2])))
            if self.coords[1][0] < overlap.coords[1][0]:
                cuboids.append(Cuboid(True, (overlap.coords[0], (self.coords[1][0], overlap.coords[1][0]), self.coords[2])))
            if overlap.coords[1][1] < self.coords[1][1]:
                cuboids.append(Cuboid(True, (overlap.coords[0], (overlap.coords[1][1], self.coords[1][1]), self.coords[2])))
            if self.coords[2][0] < overlap.coords[2][0]:
                cuboids.append(Cuboid(True, (overlap.coords[0], overlap.coords[1], (self.coords[2][0], overlap.coords[2][0]))))
            if overlap.coords[2][1] < self.coords[2][1]:
                cuboids.append(Cuboid(True, (overlap.coords[0], overlap.coords[1], (overlap.coords[2][1], self.coords[2][1]))))
            return cuboids
        else:
            return [self]

    def overlap(self, cuboid):
        all_coords = []
        for n in range(3):
            if cuboid.coords[n][0] < self.coords[n][1] and self.coords[n][0] < cuboid.coords[n][1]:
                all_coords.append((max(cuboid.coords[n][0], self.coords[n][0]), min(cuboid.coords[n][1], self.coords[n][1])))
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
            on = (parts[0] == 'on')
            coords = tuple(tuple((int(p) + n) for n, p in enumerate(part.split('=')[1].split('..'))) for part in parts[1].split(','))
            self.cuboids.append(Cuboid(on, coords))

    def cubes(self, max_coord=None):
        cuboids = []
        for cuboid in self.cuboids:
            old_cuboids = cuboids.copy()
            cuboids = []
            for old_cuboid in old_cuboids:
                cuboids.extend(old_cuboid.subtract(cuboid))
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
