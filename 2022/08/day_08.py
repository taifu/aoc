from functools import reduce


def load(data):
    trees = [[int(t) for t in line] for line in data.strip().split("\n")]
    return trees, len(trees)


def check(trees, visibles, max_tree, x, y):
    if trees[y][x] > max_tree:
        visibles.add((y, x))
    return max(max_tree, trees[y][x])


def solve1(data):
    trees, length = load(data)
    visibles = set()
    out_range = range(1, length - 1)
    int_ranges = ((0, range(1, length - 1)), (length - 1, range(length - 2, 0, -1)))
    for x in out_range:
        for dy, range_y in int_ranges:
            max_tree = trees[dy][x]
            for y in range_y:
                max_tree = check(trees, visibles, max_tree, x, y)
    for y in out_range:
        for dx, range_x in int_ranges:
            max_tree = trees[y][dx]
            for x in range_x:
                max_tree = check(trees, visibles, max_tree, x, y)
    return len(visibles) + 4 * (length - 1)


def solve2(data):
    trees, length = load(data)
    best_scenic = 0
    for x in range(1, length - 1):
        for y in range(1, length - 1):
            visibles = []
            for inc_x, inc_y in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                visibles.append(0)
                dx, dy = x, y
                while True:
                    dx += inc_x
                    dy += inc_y
                    if dx < 0 or dy < 0 or dx == length or dy == length:
                        break
                    visibles[-1] += 1
                    if trees[dy][dx] >= trees[y][x]:
                        break
            best_scenic = max(best_scenic, reduce((lambda a, b: a * b), visibles))
    return best_scenic


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
