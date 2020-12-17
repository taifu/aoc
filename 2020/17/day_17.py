from collections import defaultdict
from itertools import product


def parse(data, dimensions):
    space = set()
    for row, line in enumerate(data.strip().split('\n')):
        for col, pos in enumerate(list(line)):
            if pos == '#':
                space.add((col, row) + (0,) * (dimensions - 2))
    return space


def around(point, dimensions):
    for deltas in product(range(-1, 2), repeat=dimensions):
        yield tuple(coord + delta for coord, delta in zip(point, deltas))


def solve(data, dimensions=3, cycle=6):
    space = parse(data, dimensions)
    for cont in range(cycle):
        adjacents = defaultdict(int)
        for point in space:
            for neigh in around(point, dimensions):
                if neigh != point:
                    adjacents[neigh] += 1
        new_space = set()
        for point, tot in adjacents.items():
            if point in space:
                if tot in (2, 3):
                    new_space.add(point)
            else:
                if tot == 3:
                    new_space.add(point)
        space = new_space
    return len(space)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, 4))
