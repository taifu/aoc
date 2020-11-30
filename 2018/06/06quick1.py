from collections import deque, defaultdict

points = dict((n, tuple(int(p.strip()) for p in l.strip().split(",")))
              for n, l in enumerate(open("input.txt").readlines()))

X, Y = [max(p[0] for p in points.values()) + 1, max(p[1] for p in points.values()) + 1]


grid = [[' '] * (Y + 1) for x in range(X + 1)]


def draw(grid):
    X = len(grid)
    Y = len(grid[0])
    print("-" * (X + 2))
    for y in range(Y):
        line = "|"
        for x in range(X):
            line += grid[x][y]
        line += "|"
        print(line)
    print("-" * (X + 2))
    print()



areas = defaultdict(int)
mapped = set()
border = set()

reached = deque(points.items())
first = True
while reached:
    visited = defaultdict(set)
    while reached:
        n, point = reached.pop()
        visited[point].add(n)
    for point, ns in visited.items():
        mapped.add(point)
        if len(ns) == 1:
            n = list(ns)[0]
            areas[n] += 1
            grid[point[0]][point[1]] = chr(ord('A' if first else 'a') + n)
            if point[0] == 0 or point[1] == 0 or point[0] == X or point[1] == Y:
                border.add(n)
        else:
            grid[point[0]][point[1]] = '.'
    for point, ns in visited.items():
        while ns:
            n = ns.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if (dx or dy) and (dx == 0 or dy == 0):
                        x, y = point[0] + dx, point[1] + dy
                        if not (x < 0 or y < 0 or x > X or y > Y):
                            new_point = (x, y)
                            if new_point not in mapped:
                                reached.append((n, new_point))
    first = False
    # draw(grid)
    # print(sorted(mapped))
    # print()
    # print(sorted(reached))
    # print()
    # print(sorted(border))

# print(border)
# print(areas)

print(max(a for n, a in areas.items() if not n in border))
