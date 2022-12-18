def load(data):
    return [tuple(int(p) for p in line.split(",")) for line in data.strip().split("\n")]


class Cubes:
    def adj(self, xyz):
        for inc in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            xyz2 = tuple(xyz[n] + inc[n] for n in range(3))
            if all(self.minmax[n][0] < c < self.minmax[n][1] - 1 for n, c in enumerate(xyz2)):
                yield xyz2

    def __init__(self, data):
        self.cubes = set(data)
        self.minmax = [[999, -999] for n in range(3)]
        for xyz in self.cubes:
            self.minmax = [[min(self.minmax[n][0], xyz[n] - 1), max(self.minmax[n][1], xyz[n] + 2)] for n in range(3)]

    def outside(self):
        faces = 0
        scan = []
        # Cubes enveloping
        for x in range(*self.minmax[0]):
            for y in range(*self.minmax[1]):
                for z in range(*self.minmax[2]):
                    # Not inside
                    if sum(c in (self.minmax[n][0], self.minmax[n][1] - 1)
                           for n, c in enumerate((x, y, z))) in (1, 2):
                        scan.append((x, y, z))
        seen = set()
        while scan:
            xyz = scan.pop()
            for xyz2 in self.adj(xyz):
                if (xyz, xyz2) not in seen:
                    seen.add((xyz, xyz2))
                    if xyz2 in self.cubes:
                        faces += 1
                    else:
                        scan.append(xyz2)
        return faces

    def exposed(self):
        touching = 0
        for xyz in self.cubes:
            for xyz2 in self.adj(xyz):
                if xyz2 in self.cubes:
                    touching += 1
        return len(self.cubes) * 6 - touching


def solve1(data):
    return Cubes(load(data)).exposed()


def solve2(data):
    return Cubes(load(data)).outside()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
