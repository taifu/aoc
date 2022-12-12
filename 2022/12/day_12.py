import sys
sys.setrecursionlimit(10000)


def load(data):
    grid = []
    for line in data.strip().split("\n"):
        grid.append(line)
    return grid


class Grid:
    def __init__(self, data_grid):
        self.grid = {}
        for y, line in enumerate(data_grid):
            for x, char in enumerate(line):
                pos = x + 1j * y
                if char == 'S':
                    self.start = pos
                    self.grid[pos] = -1
                elif char == 'E':
                    self.end = pos
                    self.grid[pos] = ord('z') - ord('a') + 1
                else:
                    self.grid[pos] = ord(char) - ord('a')
        self.inf = len(self.grid)

    def search(self, pos=None, steps=None, visited=None, target=None, check_height=None, scenic=False):
        first = False
        if pos is None:
            first = True
            if scenic:
                pos = self.end
                target = 0
                check_height = lambda val: val < -1
            else:
                pos = self.start
                target = self.grid[self.end]
                check_height = lambda val: val > 1
        if steps is None:
            steps = 0
            visited = {pos: 0}
        if self.grid[pos] == target:
            return steps
        min_steps = self.inf
        for inc in (1, -1,  1j, -1j):
            next_pos = pos + inc
            if next_pos not in self.grid or check_height(self.grid[next_pos] - self.grid[pos]) or visited.get(next_pos, self.inf) <= steps + 1:
                continue
            visited[next_pos] = steps + 1
            min_steps = min(min_steps, self.search(next_pos, steps + 1, visited, target=target, check_height=check_height))
        return min_steps


def solve1(data):
    return Grid(load(data)).search()


def solve2(data):
    return Grid(load(data)).search(scenic=True)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
