def load(data):
    racksacks = []
    for line in data.strip().split("\n"):
        racksacks.append(Racksack(line))
    return racksacks


class Racksack:
    def __init__(self, line):
        middle = len(line)//2
        self.items = line[:middle], line[middle:]

    @property
    def pack(self):
        return "".join(self.items)

    def common(self, items=None):
        if not items:
            items = self.items
        first = set(items[0])
        for other in items[1:]:
            first = first.intersection(other)
        return first.pop()

    def priority(self, item=None):
        if not item:
            item = self.common()
        return (ord(item) - ord('a') + 1) if item.islower() else (ord(item) - ord('A') + 27)


def solve1(data):
    racksacks = load(data)
    return sum(racksack.priority() for racksack in racksacks)


def solve2(data):
    racksacks = load(data)
    badges = 0
    for n in range(len(racksacks)//3):
        elv1, elv2, elv3 = racksacks[n*3:(n + 1)*3]
        badges += elv1.priority(elv1.common((elv1.pack, elv2.pack,  elv3.pack)))
    return badges


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
