def load(data):
    return [tuple(int(p) for p in line.split(",")) for line in data.strip().split("\n")]


class Cubes:
    def adj(self, xyz):
        for inc in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            xyz2 = tuple(xyz[n] + inc[n] for n in range(3))
            if all(self.minmax[n][0] - 1 <= c <= self.minmax[n][1] + 1 for n, c in enumerate(xyz2)):
                yield xyz2

    def __init__(self, data):
        self.cubes = set((cube for cube in data))
        minmax = [[99, -99] for n in range(3)]
        for xyz in self.cubes:
            minmax = [[min(minmax[n][0], xyz[n]), max(minmax[n][1], xyz[n])] for n in range(3)]
        self.minmax = minmax

    def outside(self):
        faces = 0
        scan = []
        for x in range(self.minmax[0][0] - 1, self.minmax[0][1] + 2):
            for y in range(self.minmax[1][0] - 1, self.minmax[1][1] + 2):
                for z in range(self.minmax[2][0] - 1, self.minmax[2][1] + 2):
                    if (any(c in (self.minmax[n][0] - 1, self.minmax[n][1] + 1) for n, c in enumerate((x, y, z)))
                        and not all(c in (self.minmax[n][0] - 1, self.minmax[n][1] + 1) for n, c in enumerate((x, y, z)))):
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
        #whole = set((tuple(x, y, z) for x in range(20) for y in range(20) for z in range(20)))
        #return whole - self.grid 

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
