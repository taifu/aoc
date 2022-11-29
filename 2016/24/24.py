from collections import deque
import itertools
import os

raw = open("input").read()

WALL = "#"

maze = []
digits = {}

for y, l in enumerate(raw.split("\n")):
    row = list(l)
    for x, c in enumerate(row):
        if c.isdigit():
            digits[int(c)] = (x, y)
            row[x] = "."
    maze.append(row)


def print_maze(maze):
    os.system("clear")
    for row in maze:
        print("".join(row))


def shortest_path_bdf(maze, start, goal, computed={}):
    start, goal = sorted((start, goal))
    try:
        return computed[start, goal]
    except KeyError:
        pass
    size_x, size_y = len(maze[0]), len(maze)
    visited = set()
    queue = deque(((0, start),))
    while queue:
        path, pos = queue.popleft()
        if pos == goal:
            computed[start, goal] = path
            return path
        if pos in visited:
            continue
        visited.add(pos)
        # maze[pos[1]][pos[0]] = "o"
        # print_maze(maze)
        for d_x, d_y in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            new_pos = (pos[0] + d_x, pos[1] + d_y)
            try:
                if maze[new_pos[1]][new_pos[0]] != WALL:
                    queue.append((path + 1, new_pos))
            except KeyError:
                pass
    return None


shortest, shortest_path = 2**32, ""
for path in itertools.permutations(range(1, max(digits.keys()) + 1)):
    path = (0,) + path
    length = sum(shortest_path_bdf(maze, digits[path[n]], digits[path[n + 1]]) for n in range(len(path) - 1))
    if length < shortest:
         shortest = length
         shortest_path = "".join(str(n) for n in path)

print(shortest, shortest_path)

shortest, shortest_path = 2**32, ""
for path in itertools.permutations(range(1, max(digits.keys()) + 1)):
    path = (0,) + path + (0,)
    length = sum(shortest_path_bdf(maze, digits[path[n]], digits[path[n + 1]]) for n in range(len(path) - 1))
    if length < shortest:
         shortest = length
         shortest_path = "".join(str(n) for n in path)

print(shortest, shortest_path)
