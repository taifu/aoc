def load(data):
    sections = []
    for line in data.strip().split("\n"):
        parts = line.split(",")
        sections.append([int(x) for part in parts for x in part.split('-')])
    return sections


def contain(sec):
    return sec[0] >= sec[2] and sec[1] <= sec[3] or sec[2] >= sec[0] and sec[3] <= sec[1]


def overlap(sec):
    return sec[1] >= sec[2] and sec[0] <= sec[3] or sec[3] >= sec[0] and sec[2] <= sec[1]


def solve1(data):
    sections = load(data)
    return sum(1 if contain(sec) else 0 for sec in sections)


def solve2(data):
    sections = load(data)
    return sum(1 if overlap(sec) else 0 for sec in sections)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
