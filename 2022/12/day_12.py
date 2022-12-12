import sys
sys.setrecursionlimit(10000)


def load(data):
    grid = []
    for line in data.strip().split("\n"):
        grid.append(list(line))
    return grid


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if char == 'S':
                    self.start = (x, y)
                    self.grid[y][x] = -1
                elif char == 'E':
                    self.end = (x, y)
                    self.grid[y][x] = ord('z') - ord('a') + 1
                else:
                    self.grid[y][x] = ord(char) - ord('a')

    def search(self, x=None, y=None, steps=None, min_steps=None, visited=None, target=None, check_height=None, scenic=False):
        if x is None:
            if scenic:
                x, y = self.end
                target = (0, 1)
                check_height = lambda val: val < -1
            else:
                x, y = self.start
                target = (self.grid[self.end[1]][self.end[0]],)
                check_height = lambda val: val > 1
        if steps is None:
            steps = 0
            visited = {(x, y): 0}
            min_steps = self.width * self.height
        if self.grid[y][x] in target:
            return steps
        for inc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_x = x + inc[0]
            next_y = y + inc[1]
            if ((next_x < 0 or next_y < 0 or next_x == self.width or next_y == self.height) or
                check_height(self.grid[next_y][next_x] - self.grid[y][x]) or
                visited.get((next_x, next_y), self.width * self.height) <= steps + 1):
                continue
            visited[next_x, next_y] = steps + 1
            found = self.search(next_x, next_y, steps + 1, min_steps, visited, target=target, check_height=check_height, scenic=scenic)
            if found < min_steps:
                min_steps = found
        return min_steps


def solve1(data):
    return Grid(load(data)).search()


def solve2(data):
    return Grid(load(data)).search(scenic=True) + 1


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
