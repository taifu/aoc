from collections import defaultdict


class Lanterfishes:
    def __init__(self, data):
        self.families = defaultdict(int)
        for day in [int(d) for d in data.strip().split(",")]:
            self.families[day] += 1

    def live(self, days):
        for day in range(days):
            new_families = defaultdict(int)
            for day, count in sorted(self.families.items()):
                day -= 1
                if day == -1:
                    new_families[8] = count
                    day = 6
                new_families[day] += count
            self.families = new_families
        return sum(self.families.values())


def solve1(data, days=80):
    return Lanterfishes(data).live(days)


def solve2(data):
    return solve1(data, days=256)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
