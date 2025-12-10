

class Theater:
    def __init__(self, data: str) -> None:
        self.tiles: list[tuple[int, int]] = [(int(x), int(y))
                                             for x, y in (line.split(",") for line in data.strip().splitlines())]
        self.size = len(self.tiles)
        self.edges: list[tuple[int, int, int, int]] = [((xy1[0] if xy1[0] < xy2[0] else xy2[0]),
                                                        (xy1[1] if xy1[1] < xy2[1] else xy2[1]),
                                                        (xy2[0] if xy1[0] < xy2[0] else xy1[0]),
                                                        (xy2[1] if xy1[1] < xy2[1] else xy1[1]))
                                                       for xy1, xy2 in self.pairs()]

    def pairs(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        return [(self.tiles[i], self.tiles[(i+1) % self.size]) for i in range(self.size)]

    def largest(self) -> int:
        best = 0
        for n, xy1 in enumerate(self.tiles[:-1]):
            for xy2 in self.tiles[n + 1:]:
                best = max(best, (abs(xy1[0] - xy2[0]) + 1) * (abs(xy1[1] - xy2[1]) + 1))
        return best

    def intersect(self, x1:int, y1:int, x2:int, y2:int) -> bool:
        for edge in self.edges:
            if x1 < edge[2] and x2 > edge[0] and y1 < edge[3] and y2 > edge[1]:
                return True
        return False

    def largest_inside(self) -> int:
        best = 0
        for n, xy1 in enumerate(self.tiles[:-1]):
            for xy2 in self.tiles[n + 1:]:
                x1, x2 = (xy1[0], xy2[0]) if xy1[0] < xy2[0] else (xy2[0], xy1[0])
                y1, y2 = (xy1[1], xy2[1]) if xy1[1] < xy2[1] else (xy2[1], xy1[1])
                area = (x2 - x1 + 1) * (y2 - y1 + 1)
                if area > best and not self.intersect(x1, y1, x2, y2):
                    best = area
        return best


def load(data: str) -> Theater:
    return Theater(data)


def solve1(data: str) -> int:
    return load(data).largest()


def solve2(data: str) -> int:
    return load(data).largest_inside()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
