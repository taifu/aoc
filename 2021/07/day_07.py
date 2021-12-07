from collections import Counter


class Crabs:
    def __init__(self, data, inc=False):
        self.positions = Counter(int(n) for n in data.strip().split(","))
        self.min = min(self.positions.keys())
        self.max = max(self.positions.keys())
        self.inc = inc

    def dist(self, dist):
        if self.inc:
            return (dist * (dist + 1)) // 2
        return dist

    def carb(self, pos):
        tot_carb = 0
        for inc, (p, n) in enumerate(self.positions.most_common()):
            tot_carb += self.dist(abs(pos - p)) * n
        return tot_carb

    def best(self):
        less_carb = None
        start = self.positions.most_common()[0][0]
        inc = 0
        while True:
            tested = False
            for add in (-1, 1):
                pos = start + (inc * add)
                if pos >= self.min and pos <= self.max:
                    carb = self.carb(pos)
                    tested = True
            if not tested:
                break
            if less_carb is None or carb < less_carb:
                less_carb = carb
            inc += 1
        return less_carb


def solve1(data):
    return Crabs(data).best()


def solve2(data):
    return Crabs(data, inc=True).best()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
