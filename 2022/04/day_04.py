def load(data):
    sections = []
    for line in data.strip().split("\n"):
        sections.append([int(x) for sec in line.split(",") for x in sec.split('-')])
    return sections


def contain(a1, a2, b1, b2):
    return a1 >= b1 and a2 <= b2 or b1 >= a1 and b2 <= a2


def overlap(a1, a2, b1, b2):
    return a1 >= b2 and a2 <= b1 or b2 >= a1 and b1 <= a2


def solve1(data):
    sections = load(data)
    return sum(1 if contain(*sec) else 0 for sec in sections)


def solve2(data):
    sections = load(data)
    return sum(1 if overlap(*sec) else 0 for sec in sections)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
