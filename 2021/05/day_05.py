from collections import defaultdict


def interpret(line):
    return tuple(tuple(int(p) for part in line.split(" -> ")for p in part.split(",")))


def load(data):
    return tuple(interpret(line) for line in data.strip().split("\n"))


def solve1(data, diagonal=False):
    lines = load(data)
    floor = defaultdict(int)
    for x1, y1, x2, y2 in lines:
        inc_x = -1 if x2 < x1 else 1
        inc_y = -1 if y2 < y1 else 1
        for x in range(x1, x2 + inc_x, inc_x):
            if x1 == x2 or y1 == y2:
                for y in range(y1, y2 + inc_y, inc_y):
                    floor[x, y] += 1
            elif diagonal:
                floor[x, y1] += 1
                y1 += inc_y
    return sum(1 for cell in floor.values() if cell > 1)


def solve2(data):
    return solve1(data, diagonal=True)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
