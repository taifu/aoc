def load(filename):
    return [[0 if c == '.' else 1 for c in list(l.strip())] for l in open(filename).readlines()]


def left(d):
    sign = -1 if d[1] == 0 else 1
    d[0], d[1] = sign * d[1], sign * d[0]


def right(d):
    sign = -1 if d[0] == 0 else 1
    d[0], d[1] = sign * d[1], sign * d[0]


def evolve(grid, iterations, cycling=False):
    pos = [len(grid) // 2, len(grid[0]) // 2]
    direction = [0, -1]

    infections = 0
    for step in range(iterations):
        if cycling:
            if grid[pos[1]][pos[0]] == 0:  # Clean
                left(direction)
                grid[pos[1]][pos[0]] = -1
            elif grid[pos[1]][pos[0]] == -1:  # Weakened
                grid[pos[1]][pos[0]] = 1
                infections += 1
            elif grid[pos[1]][pos[0]] == 1:  # Infected
                right(direction)
                grid[pos[1]][pos[0]] = -2
            elif grid[pos[1]][pos[0]] == -2:  # Flagged
                right(direction)
                right(direction)
                grid[pos[1]][pos[0]] = 0
        else:
            if grid[pos[1]][pos[0]] == 0:
                left(direction)
            else:
                right(direction)
            grid[pos[1]][pos[0]] = 1 - grid[pos[1]][pos[0]]
            if grid[pos[1]][pos[0]] == 1:
                infections += 1
        pos = [pos[0] + direction[0], pos[1] + direction[1]]
        if pos[1] < 0:
            pos[1] = 0
            grid.insert(0, [0] * len(grid[0]))
        elif pos[1] == len(grid):
            grid.append([0] * len(grid[0]))
        elif pos[0] < 0:
            pos[0] = 0
            for row in grid:
                row.insert(0, 0)
        elif pos[0] == len(grid[0]):
            for row in grid:
                row.append(0)
    return infections


print(evolve(load("input"), 10000))
print(evolve(load("input"), 10000000, cycling=True))
