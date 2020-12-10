from collections import defaultdict


def parse(data):
    values = [int(x) for x in data.strip().split("\n")]
    return values + [max(values) + 3]


def solve(data):
    adapters = sorted(parse(data))
    differences = defaultdict(int)
    jolt = 0
    while True:
        last_jolt = jolt
        while True:
            jolt += 1
            if jolt in adapters:
                break
            if jolt > adapters[-1]:
                return differences
        differences[jolt - last_jolt] += 1
    return differences


def explore(adapters, jolt, cached):
    try:
        return cached[jolt]
    except KeyError:
        pass
    ways = 0
    for n in range(1, 4):
        if jolt + n == adapters[-1]:
            ways += 1
        elif jolt + n in adapters:
            ways += explore(adapters, jolt + n, cached)
    cached[jolt] = ways
    return ways


def solve2(data):
    return explore(sorted(parse(data)), 0, {})


if __name__ == "__main__":
    data = open("input.txt").read()
    differences = solve(data)
    print(differences[1] * differences[3])
    print(solve2(data))
