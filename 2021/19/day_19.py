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

    def rotation(self, n, cache={}):
        try:
            return cache[self.__hash__, n]
        except KeyError:
            pass
        result = frozenset(self.rotate(beacon, n) for beacon in self.beacons)
        cache[self.__hash__, n] = result
        return result

    def set_origin(self, rotation=0, delta=(0, 0, 0)):
        self.origin = tuple(p - delta[n] for n, p in enumerate(self.rotate((0, 0, 0), rotation)))


class Scanners:
    cache = {}

    def __init__(self, data):
        self.data = data
        self.scanners = [Scanner(cube) for cube in data.split('\n\n')]

    def offset(self, delta, beacons):
        return set(tuple(beacon[n] - delta[n] for n in range(3)) for beacon in beacons)

    def match_one(self, scanner, not_found=set()):
        for beacon1 in self.all_beacons:
            for rotation in NUM_ROTATIONS:
                if (beacon1, rotation, scanner) in not_found:
                    continue
                beacons = scanner.rotation(rotation)
                for beacon2 in beacons:
                    delta = tuple((beacon2[n] - beacon1[n]) for n in range(3))
                    offset_beacons = self.offset(delta, beacons)
                    if len(offset_beacons.intersection(self.all_beacons)) >= 12:
                        return True, rotation, delta, offset_beacons
                else:
                    not_found.add((beacon1, rotation, scanner))
        return False, None, None, None

    def match_all(self):
        try:
            self.all_beacons, self.all_origins = Scanners.cache[self.data]
            return
        except KeyError:
            pass
        scanner, *scanners = self.scanners
        scanner.set_origin()
        self.all_beacons = scanner.beacons.copy()
        self.all_origins = [scanner.origin]
        while scanners:
            for scanner in scanners:
                found, rotation, delta, offset_beacons = self.match_one(scanner)
                if found:
                    scanner.set_origin(rotation, delta)
                    scanners.remove(scanner)
                    self.all_beacons |= offset_beacons
                    self.all_origins.append(scanner.origin)
            print(len(self.all_beacons), len(scanners))
        Scanners.cache[self.data] = self.all_beacons, self.all_origins


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
