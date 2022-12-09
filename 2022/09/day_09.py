from math import copysign


def load(data):
    return [(line[0], int(line[2:])) for line in data.strip().split("\n")]


def follow(head, tail):
    moving = [abs(head[n] - tail[n]) for n in range(2)]
    if max(moving) == 2:
        for n in range(2):
            tail[n] += int(copysign(min(1, moving[n]), head[n] - tail[n]))


def move(moves, length):
    grid, knots = set(((0, 0),)), [[0, 0] for n in range(length)]
    for direction, step in moves:
        incs = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}[direction]
        for n in range(step):
            for xy in range(2):
                knots[0][xy] += incs[xy]
            for head, tail in zip(knots, knots[1:]):
                follow(head, tail)
            grid.add(tuple(knots[-1]))
    return grid


def solve1(data):
    return len(move(load(data), 2))


def solve2(data):
    return len(move(load(data), 10))


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
