from collections import Counter


class Crabs:
    def __init__(self, data, inc=False):
        self.positions = Counter(int(n) for n in data.strip().split(","))
        self.start = min(self.positions.keys())
        self.max = max(self.positions.keys())
        self.inc = inc

    def dist(self, dist):
        if self.inc:
            return (dist * (dist + 1)) // 2
        return dist

    def carb(self, pos):
        tot_carb = 0
        for inc, (p, n) in enumerate(self.positions.items()):
            tot_carb += self.dist(abs(pos - p)) * n
        return tot_carb

    def best(self):
        less_carb = None
        for pos in range(self.start, self.max + 1):
            carb = self.carb(pos)
            if less_carb is None or carb < less_carb:
                less_carb = carb
        return less_carb


def solve1(data):
    return Crabs(data).best()


def solve2(data):
    return Crabs(data, inc=True).best()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
