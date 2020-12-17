from itertools import product


def parse(data, dimensions):
    return set(((col, row) + (0,) * (dimensions - 2))
               for row, line in enumerate(data.strip().split('\n'))
               for col, pos in enumerate(line) if pos == '#')


def around(point, dimensions):
    for deltas in product(range(-1, 2), repeat=dimensions):
        yield tuple(coord + delta for coord, delta in zip(point, deltas))


def solve(data, dimensions=3, cycle=6):
    space = parse(data, dimensions)
    for cont in range(cycle):
        adjacents = {}
        for point in space:
            for neigh in around(point, dimensions):
                if neigh != point:
                    try:
                        adjacents[neigh] += 1
                    except KeyError:
                        adjacents[neigh] = 1
        space = set(point for point, tot in adjacents.items() if tot == 3 or point in space and tot == 2)
    return len(space)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, 4))
