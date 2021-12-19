import itertools


# See rotations.py
ALL_ROTATIONS = (
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (y, -z, -x),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-z, -y, -x),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (-z, x, -y),
    lambda x, y, z: (-y, -x, -z),
)
NUM_ROTATIONS = tuple(range(len(ALL_ROTATIONS)))


class Scanner:
    def __init__(self, cube):
        self.beacons = set(tuple(int(n) for n in point.split(',')) for point in cube.strip().split('\n')[1:])
        self.origin = None

    def rotate(self, beacon, rotation):
        return ALL_ROTATIONS[rotation](*beacon)

    def rotations(self):
        for n in NUM_ROTATIONS:
            yield n, set(self.rotate(beacon, n) for beacon in self.beacons)

    def set_origin(self, rotation=0, delta=(0, 0, 0)):
        self.origin = tuple(p - delta[n] for n, p in enumerate(self.rotate((0, 0, 0), rotation)))


class Scanners:
    cache = {}

    def __init__(self, data):
        self.data = data
        self.scanners = [Scanner(cube) for cube in data.split('\n\n')]

    def offset(self, delta, beacons):
        return set(tuple(beacon[n] - delta[n] for n in range(3)) for beacon in beacons)

    def match_all(self):
        try:
            self.all_beacons, self.all_origins = Scanners.cache[self.data]
            return
        except KeyError:
            pass
        scanner = self.scanners.pop(0)
        scanner.set_origin()
        positioned = [scanner]
        self.all_beacons = scanner.beacons.copy()
        self.all_origins = [scanner.origin]
        import time
        s = time.time()
        while self.scanners:
            print(time.time() - s, len(self.all_beacons), len(self.scanners))
            s = time.time()
            found = False
            for scanner in self.scanners:
                for rotation, beacons in scanner.rotations():
                    for beacon1 in self.all_beacons:
                        for beacon2 in beacons:
                            delta = tuple((beacon2[n] - beacon1[n]) for n in range(3))
                            offset_beacons = self.offset(delta, beacons)
                            if len(offset_beacons.intersection(self.all_beacons)) >= 12:
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                positioned.append(scanner)
                scanner.set_origin(rotation, delta)
                self.scanners.remove(scanner)
                self.all_beacons |= offset_beacons
                self.all_origins.append(scanner.origin)
        Scanners.cache[self.data] = self.scanners, self.all_origins


def solve1(data):
    scanners = Scanners(data)
    scanners.match_all()
    return len(scanners.all_beacons)


def solve2(data):
    scanners = Scanners(data)
    scanners.match_all()
    max_dist = 0
    for origin_1, origin_2 in itertools.combinations(scanners.all_origins, 2):
        dist = sum(abs(origin_1[n] - origin_2[n]) for n in range(3))
        if dist > max_dist:
            max_dist = dist
    return max_dist


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
