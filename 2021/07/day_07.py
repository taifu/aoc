from collections import Counter


class Crabs:
    def __init__(self, data):
        self.positions = Counter(int(n) for n in data.strip().split(","))
        self.pos = min(self.positions.keys())

    def dist(self, dist, inc):
        return (dist * (dist + 1)) // 2 if inc else dist

    def carb(self, pos, inc):
        return sum(self.dist(abs(pos - p), inc) * n for p, n in self.positions.items())

    def best(self, inc=False):
        prev_carb = float("inf")
        while True:
            carb = self.carb(self.pos, inc)
            if prev_carb < carb:
                return prev_carb
            prev_carb = carb
            self.pos += 1


def solve1(data):
    return Crabs(data).best()


def solve2(data):
    return Crabs(data).best(inc=True)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
