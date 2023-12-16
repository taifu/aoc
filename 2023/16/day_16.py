from collections import defaultdict, deque


class Contraption:
    def __init__(self, raw: str):
        self.map = [list(line) for line in raw.splitlines()]
        self.height = len(self.map)
        self.width = len(self.map[0])

    def energy(self, x: int = -1, y: int = 0, dx: int = 1, dy: int = 0) -> int:
        visited: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
        rays = deque(((x, y, dx, dy),))
        while rays:
            x, y, dx, dy = rays.popleft()
            while True:
                x += dx
                y += dy
                if x < 0 or x >= self.width or y < 0 or y >= self.height:
                    break
                if (dx, dy) in visited[(x, y)]:
                    break
                cell = self.map[y][x]
                visited[(x, y)].add((dx, dy))
                if cell == '-' and dy != 0:
                    rays.append((x, y, -1, 0))
                    rays.append((x, y, 1, 0))
                    break
                elif cell == '|' and dx != 0:
                    rays.append((x, y, 0, -1))
                    rays.append((x, y, 0, 1))
                    break
                elif cell == '/':
                    if dx != 0:
                        dx, dy = dy, -dx
                    else:
                        dx, dy = -dy, dx
                elif cell == '\\':
                    if dx != 0:
                        dx, dy = dy, dx
                    else:
                        dx, dy = dy, dx
        return sum(1 for energy in visited.items() if energy)

    def max_energy(self) -> int:
        max_energy = 0
        for y in (-1, self.height):
            for x in range(self.width):
                max_energy = max(max_energy, self.energy(x, y, 0, 1 if y == -1 else -1))
        for x in (-1, self.width):
            for y in range(self.height):
                max_energy = max(max_energy, self.energy(x, y, 1 if x == -1 else -1, 0))
        return max_energy


def solve1(data: str) -> int:
    return Contraption(data).energy()


def solve2(data: str) -> int:
    return Contraption(data).max_energy()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
