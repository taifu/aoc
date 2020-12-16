from collections import defaultdict


def parse(data):
    values = [int(x) for x in data.strip().split("\n")]
    return sorted(values) + [max(values) + 3]


def solve1(data):
    adapters = parse(data)
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


def explore(adapters, jolt, cached):
    try:
        return cached[jolt]
    except KeyError:
        ways = 0
        for n in range(1, 4):
            if jolt + n == adapters[-1]:
                ways += 1
            elif jolt + n in adapters:
                ways += explore(adapters, jolt + n, cached)
        cached[jolt] = ways
        return ways


def solve2(data):
    return explore(parse(data), 0, {})


if __name__ == "__main__":
    data = open("input.txt").read()
    differences = solve1(data)
    print(differences[1] * differences[3])
    print(solve2(data))
