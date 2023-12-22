from operator import methodcaller


X, Y, Z = 0, 1, 2


class Brick:
    def __init__(self, line: str):
        self.coord, coord_to = [[int(d) for d in part.split(',')] for part in line.split('~')]
        assert len(set(self.coord + coord_to)) <= 4
        assert all(self.coord[n] <= coord_to[n] for n in range(3))
        self.lengths = [coord_to[n] - self.coord[n] + 1 for n in range(3)]
        self.supports: set[Brick] = set()
        self.supported_by: set[Brick] = set()

    def key(self) -> int:
        return self.coord[Z]

    def intersects(self, other: "Brick") -> bool:
        return not (self.coord[0] >= other.coord[0] + other.lengths[0] or  # noqa: W504
                    self.coord[0] + self.lengths[0] <= other.coord[0] or  # noqa: W504
                    self.coord[1] >= other.coord[1] + other.lengths[1] or  # noqa: W504
                    self.coord[1] + self.lengths[1] <= other.coord[1])


class Snapshot:
    def __init__(self) -> None:
        self.loaded = False

    def load(self, raw: str) -> None:
        self.loaded = True
        self.bricks = [Brick(line) for line in raw.splitlines()]
        self.max = [max(b.coord[n] + b.lengths[n] for b in self.bricks) for n in (X, Y)]
        self.fall()
        self.build_support_relations()

    def fall(self) -> None:
        occupied = [[0 for x in range(self.max[X])] for y in range(self.max[Y])]
        for brick in sorted(self.bricks, key=methodcaller('key')):
            if brick.lengths[X] > 1:
                max_z = max(occupied[brick.coord[Y]][x] for x in range(brick.coord[X], brick.coord[X] + brick.lengths[X]))
            elif brick.lengths[Y] > 1:
                max_z = max(occupied[y][brick.coord[X]] for y in range(brick.coord[Y], brick.coord[Y] + brick.lengths[Y]))
            else:
                max_z = occupied[brick.coord[Y]][brick.coord[X]]
            brick.coord[Z] = max_z + 1
            for y in range(brick.coord[Y], brick.coord[Y] + brick.lengths[Y]):
                for x in range(brick.coord[X], brick.coord[X] + brick.lengths[X]):
                    occupied[y][x] = max_z + brick.lengths[Z]

    def build_support_relations(self) -> None:
        for n, brick_1 in enumerate(self.bricks):
            for brick_2 in self.bricks[n + 1:]:
                if brick_1.intersects(brick_2):
                    for brick_below, brick_above in ((brick_1, brick_2), (brick_2, brick_1)):
                        if brick_below.coord[Z] + brick_below.lengths[Z] == brick_above.coord[Z]:
                            brick_below.supports.add(brick_above)
                            brick_above.supported_by.add(brick_below)
                            break

    def how_many_disintegrable(self) -> int:
        return sum(1 for brick in self.bricks if all(len(b.supported_by) > 1 for b in brick.supports))

    def explore(self, brick: Brick, falling: set[Brick]) -> None:
        if brick in falling:
            return
        falling.add(brick)
        for brick_over in brick.supports:
            if not (brick_over.supported_by - falling):
                self.explore(brick_over, falling)

    def how_many_falling(self) -> int:
        total = 0
        for brick in self.bricks:
            falling: set[Brick] = set()
            self.explore(brick, falling)
            total += len(falling) - 1
        return total


snapshot = Snapshot()


def solve1(data: str) -> int:
    snapshot.load(data)
    return snapshot.how_many_disintegrable()


def solve2(data: str) -> int:
    if not snapshot.loaded:
        snapshot.load(data)
    return snapshot.how_many_falling()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
