def load(data):
    return [(line[0], int(line[2:])) for line in data.strip().split("\n")]


def draw(knots):
    import time
    print("\033[0;0H")
    size_x, size_y = 60, 30
    matrix = [[' '] * size_x for n in range(size_y)]
    for n, n_knot in enumerate(range(len(knots) - 1, -1, -1)):
        char = 'T' if n == 0 else 'H' if n == len(knots) - 1 else str(len(knots) - n)
        matrix[(knots[n_knot][1] + size_y // 2) % size_y][(knots[n_knot][0] + size_x // 2) % size_x] = char
    header = f"+{'-' * size_x}+"
    print(header)
    for line in matrix:
        print(f"|{''.join(line)}|")
    print(header)
    time.sleep(0.01)


def follow(head, tail):
    moving = [head[n] - tail[n] for n in range(2)]
    if max(map(abs, moving)) == 2:
        for n in range(2):
            tail[n] += round((moving[n] * 1.1) / 2)


def move(moves, length, drawing=False):
    grid, knots = set(((0, 0),)), [[0, 0] for n in range(length)]
    for direction, step in moves:
        incs = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}[direction]
        for n in range(step):
            for xy in range(2):
                knots[0][xy] += incs[xy]
            for head, tail in zip(knots, knots[1:]):
                follow(head, tail)
            if drawing:
                draw(knots)
            grid.add(tuple(knots[-1]))
    return grid


def solve1(data):
    return len(move(load(data), 2))


def solve2(data, drawing=False):
    return len(move(load(data), 10, drawing))


if __name__ == "__main__":
    import sys
    data = open("input.txt").read()

    print(solve1(data))
    print(solve2(data, True if '-d' in sys.argv else False))
