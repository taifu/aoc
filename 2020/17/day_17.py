from itertools import product


def parse(data, dimensions):
    space = {}
    for row, line in enumerate(data.strip().split('\n')):
        for col, pos in enumerate(list(line)):
            if pos == '#':
                space[(row, col) + (0,) * (dimensions - 2)] = 1
    return space


def around(point, dimensions):
    for deltas in product(range(-1, 2), repeat=dimensions):
        yield tuple(coord + delta for coord, delta in zip(point, deltas))


def solve(data, dimensions=3, cycle=6):
    space = parse(data, dimensions)
    for cont in range(cycle):
        new_space, visited = {}, set()
        for point in space.keys():
            for new in around(point, dimensions):
                if new in visited:
                    continue
                visited.add(new)
                current = space.get(new, 0)
                active = sum(space.get(neigh, 0) for neigh in around(new, dimensions)) - current
                if current == 1 and active in (2, 3) or active == 3:
                    new_space[new] = 1
        space = new_space
    return sum(space.values())


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, 4))
