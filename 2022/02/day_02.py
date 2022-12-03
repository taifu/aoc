def load(data):
    steps = []
    for line in data.strip().split("\n"):
        parts = line.split()
        steps.append(parts)
    return steps


def point(their, your):
    outcome = {('A', 'X'): 3, ('B', 'Y'): 3, ('C', 'Z'): 3,
               ('A', 'Y'): 6, ('B', 'Z'): 6, ('C', 'X'): 6}.get((their, your), 0)
    return outcome + {'X': 1, 'Y': 2, 'Z': 3}[your]


def strategy(their, your):
    return {('A', 'X'): 'Z', ('B', 'X'): 'X', ('C', 'X'): 'Y',
            ('A', 'Y'): 'X', ('B', 'Y'): 'Y', ('C', 'Y'): 'Z',
            ('A', 'Z'): 'Y', ('B', 'Z'): 'Z', ('C', 'Z'): 'X'}.get((their, your))


def solve1(data):
    steps = load(data)
    points = 0
    for their, your in steps:
        points += point(their, your)
    return points


def solve2(data):
    steps = load(data)
    points = 0
    for their, your in steps:
        points += point(their, strategy(their, your))
    return points


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
