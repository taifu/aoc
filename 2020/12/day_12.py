import math


POINTS = "ESWN"
EAST, SOUTH, WEST, NORTH = POINTS
FORWARD, RIGHT, LEFT = "FRL"


def parse(data):
    return [(line[0], int(line[1:].strip())) for line in data.strip().split("\n")]


def increments(direction):
    return {EAST: (1, 0), SOUTH: (0, -1), WEST: (-1, 0), NORTH: (0, 1)}[direction]


def rotate(point, degrees):
    """
    Rotate a point clockwise by a given angle around a given origin.
    The angle should be given in degree.
    """
    ox, oy = 0, 0
    px, py = point

    angle = math.radians(-degrees)

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return int(round(qx, 5)), int(round(qy, 5))


def solve2(data):
    pos = [0, 0]
    pos_w = [10, 1]

    for action, step in parse(data):
        if action in (RIGHT, LEFT):
            if action == LEFT:
                step = 360 - step
            pos_w = rotate(pos_w, step)
            continue
        if action == FORWARD:
            pos = [pos[0] + pos_w[0] * step, pos[1] + pos_w[1] * step]
        else:
            incrs = increments(action)
            pos_w = [pos_w[0] + incrs[0] * step, pos_w[1] + incrs[1] * step]
    return sum(abs(x) for x in pos)


def solve1(data):
    pos = [0, 0]
    # EAST=0 SOUTH=1 WEST=2 NORTH=3
    direction = POINTS.index(EAST)

    for action, step in parse(data):
        if action in (RIGHT, LEFT):
            direction = int((direction + (1 if action == RIGHT else - 1) * step / 90) % 4)
            continue
        if action == "F":
            incrs = increments(POINTS[direction])
        else:
            incrs = increments(action)
        pos = [pos[0] + incrs[0] * step, pos[1] + incrs[1] * step]
    return sum(abs(x) for x in pos)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
