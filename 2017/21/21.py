def tupint(raw):
    return tuple(0 if c == '.' else 1 for c in raw if c in '.#')


def load(filename):
    rules = {}
    for l in open(filename).readlines():
        old, new = l.strip().split(" => ")
        rules[tupint(old)] = tupint(new)
    return rules


def start():
    return [[0, 1, 0], [0, 0, 1], [1, 1, 1]]


def get(rules, key):
    if len(key) == 4:
        for idx in ((0, 1, 2, 3), (1, 3, 0, 2), (3, 2, 1, 0), (2, 0, 3, 1),
                    (1, 0, 3, 2), (0, 2, 1, 3), (2, 3, 0, 1), (3, 1, 2, 0)):
            try:
                return rules[tuple(key[i] for i in idx)]
            except KeyError:
                pass
    elif len(key) == 9:
        for idx in ((0, 1, 2, 3, 4, 5, 6, 7, 8), (2, 5, 8, 1, 4, 7, 0, 3, 6),
                    (8, 7, 6, 5, 4, 3, 2, 1, 0), (6, 3, 0, 7, 4, 1, 8, 5, 2),
                    (2, 1, 0, 5, 4, 3, 8, 7, 6), (8, 5, 2, 7, 4, 1, 6, 3, 0),
                    (6, 7, 8, 3, 4, 5, 0, 1, 2), (0, 3, 6, 1, 4, 7, 2, 5, 8)):
            try:
                return rules[tuple(key[i] for i in idx)]
            except KeyError:
                pass
    raise Exception("{} not found in {}".format(key, rules.keys()))


def evolve(grid, rules, iterations):
    for i in range(iterations):
        old_size, new_size = (2, 3) if len(grid) % 2 == 0 else (3, 4)
        size = len(grid) // old_size * new_size
        new_grid = [[0 for n in range(size)] for m in range(size)]
        for dy in range(0, len(grid), old_size):
            for dx in range(0, len(grid), old_size):
                rule = get(rules, tuple(grid[y][x] for y in range(dy, dy + old_size) for x in range(dx, dx + old_size)))
                i = 0
                for y in range(dy // old_size * new_size, dy // old_size * new_size + new_size):
                    for x in range(dx // old_size * new_size, dx // old_size * new_size + new_size):
                        new_grid[y][x] = rule[i]
                        i += 1
        grid = new_grid
    return grid

grid = evolve(start(), load("input"), 5)
print(sum(sum(row) for row in grid))


grid = evolve(start(), load("input"), 18)
print(sum(sum(row) for row in grid))
