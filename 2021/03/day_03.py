def load(data):
    return [tuple(line) for line in data.strip().split("\n")]


def find_commons(bits, most=True):
    length = len(bits[0])
    commons = ()
    find = (1, 0) if most else (0, 1)
    for n in range(length):
        tot1 = sum(int(line[n]) for line in bits)
        commons += (find[0] if tot1 >= (len(bits) + 1) // 2 else find[1],)
    return commons, length


def solve1(data):
    commons, length = find_commons(load(data))
    gamma = int("".join(str(c) for c in commons), 2)
    epsilon = 2**length - gamma - 1
    return epsilon * gamma


def solve2(data):
    ratings = []
    for gen in range(2):
        bits, pos = load(data), 0
        while len(bits) > 1:
            commons, length = find_commons(bits, gen == 0)
            bits = [line for line in bits if int(line[pos]) == commons[pos]]
            pos += 1
        ratings.append("".join(bits[0]))
    return int(ratings[0], 2) * int(ratings[1], 2)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
