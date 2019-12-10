from fractions import Fraction


class Asteroids:
    TURNS = ((1, -1), (1, 1), (-1, 1), (-1, -1))

    def __init__(self, asteroids):
        self.asteroids = set()
        rows = asteroids.strip().split("\n")
        self.width, self.height = len(rows[0]), len(rows)
        self.size = max(self.width, self.height)
        for y, row in enumerate(rows):
            for x, cell in enumerate(row.strip()):
                if cell == "#":
                    self.asteroids.add((x, y))

    def inside(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        return True

    def count_visibles(self, x, y):
        left = self.asteroids.copy()
        try:
            left.remove((x, y))
        except KeyError:
            pass
        for p1 in range(self.size):
            for p2 in range(self.size):
                if p1 == p2 == 0:
                    continue
                for n, (m1, m2) in enumerate(self.TURNS):
                    dx, dy = p1 * m1, p2 * m2
                    if n % 2 == 1:
                        dx, dy = dy, dx
                    next_x, next_y = x, y
                    seen = False
                    while True:
                        next_x += dx
                        next_y += dy
                        if not self.inside(next_x, next_y):
                            break
                        if (next_x, next_y) in left:
                            if seen:
                                left.remove((next_x, next_y))
                            else:
                                seen = True
        return len(left)

    def show(self, asteroids=None):
        all_map = [['.'] * self.width for n in range(self.height)]
        for x, y in (asteroids or self.asteroids):
            all_map[y][x] = '#'
        for row in all_map:
            print("".join(row))

    def best(self):
        max_visibles = (0,)
        for x, y in self.asteroids:
            visibles = self.count_visibles(x, y)
            if visibles > max_visibles[0]:
                max_visibles = (visibles, x, y)
        return max_visibles

    def visibles(self, x, y, left=None):
        if left is None:
            left = self.asteroids.copy()
        try:
            left.remove((x, y))
        except KeyError:
            pass
        coefficients = set()
        inf = float('inf')
        checked = set()
        all_seen = []
        for n, (m1, m2) in enumerate(self.TURNS):
            turn_seen = []
            for p1 in range(self.size):
                for p2 in range(self.size):
                    if p1 == p2 == 0:
                        continue
                    dx, dy = p1 * m1, p2 * m2
                    if n % 2 == 1:
                        dx, dy = dy, dx
                    if (dx, dy) in checked:
                        continue
                    checked.add((dx, dy))
                    if dx == 0:
                        coefficient = (inf if dy > 0 else -inf, m1)
                    else:
                        coefficient = (Fraction(dy, dx), m1)
                    if coefficient in coefficients:
                        continue
                    coefficients.add(coefficient)
                    next_x, next_y = x, y
                    while True:
                        next_x += dx
                        next_y += dy
                        if not self.inside(next_x, next_y):
                            break
                        if (next_x, next_y) in left:
                            turn_seen.append((coefficient, next_x, next_y))
                            break
            all_seen += [(x, y) for c, x, y in sorted(turn_seen)]
        return all_seen

    def shoot(self, x, y):
        left = self.asteroids.copy()
        all_visibles = []
        while left:
            visibles = self.visibles(x, y, left)
            assert visibles
            left = left - set(visibles)
            all_visibles += visibles
        return all_visibles


def test():
    ast = Asteroids("""#.........
...#......
...#..#...
.####....#
..#.#.#...
.....#....
..###.#.##
.......#..
....#...#.
...#..#..#""")
    assert ast.count_visibles(0, 0) == 7

    ast = Asteroids(""".#..#
.....
#####
....#
...##""")
    assert ast.best() == (8, 3, 4)

    ast = Asteroids("""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""")
    assert ast.best() == (33, 5, 8)

    ast = Asteroids(""".#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##""")
    assert ast.visibles(8, 3)[:2] == [(8, 1), (9, 0)]
    ast.shoot(8, 3)

    ast = Asteroids(""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""")
    assert ast.best() == (210, 11, 13)
    visibles = ast.shoot(11, 13)
    assert visibles[199] == (8, 2)


if __name__ == "__main__":
    ast = Asteroids(open("input.txt").read())
    best = ast.best()
    print(best[0])
    visibles = ast.shoot(best[1], best[2])
    a200 = visibles[199]
    print(a200[0] * 100 + a200[1])
