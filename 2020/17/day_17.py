def parse(data, four_dimensions):
    space = {}
    for row, line in enumerate(data.strip().split('\n')):
        for col, pos in enumerate(list(line)):
            if pos == '#':
                space[(row, col, 0) + ((0,) if four_dimensions else ())] = 1
    return space


def around(point, four_dimensions, this_included=False):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if four_dimensions:
                    for dw in range(-1, 2):
                        if this_included or not (dx == 0 and dy == 0 and dz == 0 and dw == 0):
                            yield point[0] + dx, point[1] + dy, point[2] + dz, point[3] + dw
                else:
                    if this_included or not (dx == 0 and dy == 0 and dz == 0):
                        yield point[0] + dx, point[1] + dy, point[2] + dz


def solve(data, four_dimensions=False):
    space = parse(data, four_dimensions)
    for cont in range(6):
        new_space = {}
        for point, current in space.items():
            for new_point in around(point, four_dimensions, this_included=True):
                active = sum(space.get(around_point, 0) for around_point in around(new_point, four_dimensions))
                if space.get(new_point, 0) == 1 and active in (2, 3) or active == 3:
                    new_space[new_point] = 1
        space = new_space
    return sum(space.values())


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, True))
