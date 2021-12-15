import bisect


class Cave:
    def __init__(self, data, mult=1):
        matrix = tuple(tuple(int(n) for n in line) for line in data.strip().split("\n"))
        matrix_size = len(matrix)
        self.size = matrix_size * mult
        self.chitons = [[(matrix[y % matrix_size][x % matrix_size] + x // matrix_size + y // matrix_size - 1) % 9 + 1
                         for x in range(self.size)] for y in range(self.size)]

    def adj(self, x, y):
        for x0, y0 in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if y0 < 0 or y0 >= self.size or x0 < 0 or x0 >= self.size:
                continue
            yield x0, y0

    def dijkstra(self, exploring):
        weights = {}
        while exploring:
            prev_path, x, y = exploring.pop(0)
            path = prev_path + self.chitons[y][x]
            if (x, y) not in weights or path < weights[x, y]:
                weights[x, y] = path
                if x == y == self.size - 1:
                    return weights[x, y] - weights[0, 0]
            else:
                continue
            for x0, y0 in self.adj(x, y):
                bisect.insort(exploring, (path, x0, y0))

    def best(self):
        return self.dijkstra([(0, 0, 0)])


def solve1(data):
    return Cave(data).best()


def solve2(data):
    return Cave(data, 5).best()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
