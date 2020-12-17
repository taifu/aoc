def parse(data, dimensions):
    space = set()
    for row, line in enumerate(data.strip().split('\n')):
        for col, pos in enumerate(list(line)):
            if pos == '#':
                space.add((col, row) + (0,) * (dimensions - 2))
    return space


def solve1(data):
    pass


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    #print(solve2(data))
