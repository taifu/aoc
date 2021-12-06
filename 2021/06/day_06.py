from collections import defaultdict


class Lanterfishes:
    def __init__(self, days):
        self.families = defaultdict(int)
        for day in days:
            self.families[day] += 1

    def live(self):
        new_families = defaultdict(int)
        for day, count in sorted(self.families.items()):
            day -= 1
            if day == -1:
                new_families[8] = count
                day = 6
            new_families[day] += count
        self.families = new_families

    def count(self):
        return sum(self.families.values())


def load(data):
    return Lanterfishes([int(d) for d in data.strip().split(",")])


def solve1(data, days=80):
    lanterfishes = load(data)
    for day in range(days):
        lanterfishes.live()
    return lanterfishes.count()


def solve2(data):
    return solve1(data, days=256)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
