from collections import Counter, defaultdict


class Polymer:
    def __init__(self, data):
        template, lines = [p.strip().split("\n") for p in data.strip().split("\n\n")]
        self.template = template[0]
        self.rules = {}
        for line in lines:
            p1, c3 = line.split(" -> ")
            c1, c2 = tuple(p1)
            self.rules[c1, c2] = [((c1, c3), 1), ((c3, c2), 1), (c3, -1)]
        self.count = defaultdict(int)
        self.letters = defaultdict(int)
        for c1, c2 in zip(self.template, self.template[1:]):
            self.count[(c1, c2)] += 1
            self.letters[c2] -= 1
        self.letters[c2] += 1

    def most_common(self, steps):
        for step in range(steps):
            next_count = defaultdict(int)
            for n, (left, how_many) in enumerate(self.count.items()):
                if len(left) == 2:
                    for what, add in self.rules[left]:
                        next_count[what] += add * how_many
                else:
                    self.letters[left] += how_many
            self.count = next_count
        for left, how_many in self.count.items():
            if len(left) == 2:
                self.letters[left[0]] += how_many
                self.letters[left[1]] += how_many
            else:
                self.letters[left] += how_many
        most_common = Counter(self.letters).most_common()
        return most_common[0][1] - most_common[-1][1]


def solve1(data):
    return Polymer(data).most_common(10)


def solve2(data):
    return Polymer(data).most_common(40)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
