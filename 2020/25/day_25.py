def step(p, n):
    return (p * n) % 20201227


def loop_size(e):
    n, m, s = 7, 1, 0
    while True:
        if m == e:
            return s
        m = step(m, n)
        s += 1


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
