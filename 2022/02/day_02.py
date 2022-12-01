from collections import defaultdict


def load(data):
    elves = defaultdict(list)
    cont = 0
    for line in data.strip().split("\n"):
        cal = int(line.strip() or "0")
        if not cal:
            cont += 1
        elves[cont].append(cal)
    return elves


def solve1(data):
    most = 0
    for elves, items in load(data).items():
        most = max(most, sum(items))
    return most


def solve2(data):
    mostest = []
    for elves, items in load(data).items():
        mostest.append(sum(items))
    return sum(list(reversed(sorted(mostest)))[:3])


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
