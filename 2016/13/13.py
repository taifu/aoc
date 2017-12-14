from collections import deque


def maze(val, x, y):
    def wall(val, x, y):
        n = x**2 + 3 * x + 2 * x * y + y + y * y + val
        bits = sum(1 if c == "1" else 0 for c in bin(n))
        return 1 if bits % 2 == 1 else 0

    grid = [[wall(val, i, j) for i in range(x)] for j in range(y)]
    return grid


def minimum_path_bfs(grid, pos, target):
    queue = deque([("", pos)])
    visited = set()
    while queue:
        path, current = queue.popleft()
        if current == target:
            return path
        if current in visited:
            continue
        visited.add(current)
        for new_path, d_x, d_y in (("n", 0, -1), ("s", 0, 1), ("e", -1, 0), ("w", 1, 0)):
            new_pos = (current[0] + d_x, current[1] + d_y)
            if new_pos[0] >= 0 and new_pos[0] <= len(grid[0]) and new_pos[1] >= 0 and new_pos[1] <= len(grid):
                if grid[new_pos[1]][new_pos[0]] == 0:
                    queue.append((path + new_path, new_pos))
    return ""


grid = maze(10, 30, 30)
path = minimum_path_bfs(grid, (1, 1), (7, 4))
print(len(path), path)

grid = maze(1364, 100, 100)
path = minimum_path_bfs(grid, (1, 1), (31, 39))
print(len(path), path)

max_50 = 1
for x in range(55):
    for y in range(55):
        path = minimum_path_bfs(grid, (1, 1), (x, y))
        if path > "" and len(path) <= 50:
            max_50 += 1
print(max_50)


