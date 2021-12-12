from collections import defaultdict


class Caves:
    def __init__(self, data):
        self.edges = defaultdict(list)
        for edge in data.strip().split("\n"):
            v1, v2 = edge.split("-")
            if v2 != 'start' and v1 != 'end':
                self.edges[v1].append(v2)
            if v2 != 'end' and v1 != 'start':
                self.edges[v2].append(v1)

    def count(self, cave, visited, double_cave=False):
        if cave == 'end':
            return 1
        if cave.islower() and cave in visited:
            if double_cave is False or double_cave:
                return 0
            double_cave = cave
        return sum(self.count(next_cave, visited | {cave}, double_cave)
                   for next_cave in self.edges[cave])

    def paths(self, double=False):
        return self.count('start', set(), double)


def solve1(data):
    return Caves(data).paths()


def solve2(data):
    return Caves(data).paths(None)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
