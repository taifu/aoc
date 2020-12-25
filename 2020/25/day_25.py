def step(p, n):
    r = 20201227
    return (p * n) % r


def loop_size(e):
    n = m = 7
    s = 1
    while True:
        s += 1
        m = step(m, n)
        if m == e:
            return s


def transform(m, s):
    n = m
    for i in range(s - 1):
        m = step(m, n)
    return m


def parse(data):
    return list(int(n) for n in data.strip().split('\n'))


def solve(data):
    card, door = parse(data)
    return transform(door, loop_size(card))


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
