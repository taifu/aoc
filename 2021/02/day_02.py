def interpret(row):
    action, step = row.split(" ")
    step = int(step)
    if action == 'forward':
        op = (1, 0)
    elif action == 'down':
        op = (0, 1)
    elif action == 'up':
        op = (0, -1)
    else:
        raise Exception(row)
    return op, step


def load(data):
    return [interpret(line) for line in data.strip().split("\n")]


def solve1(data, aim=None):
    depth, horiz = 0, 0
    for op, step in load(data):
        if aim is None:
            horiz += op[0] * step
            depth += op[1] * step
        else:
            aim += op[1] * step
            horiz += op[0] * step
            depth += op[0] * aim * step
    return depth * horiz


def solve2(data):
    return solve1(data, aim=0)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
