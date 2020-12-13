def parse(data):
    lines = data.strip().split()
    time = int(lines[0])
    busses = [int(x) if x.isdigit() else 0 for x in lines[1].strip().split(',')]
    return time, busses


def solve(data):
    time, busses = parse(data)
    best_rest = (time, 0)
    for bus in busses:
        if bus == 0:
            continue
        loop = int(time / bus)
        rest = ((loop + 1) * bus) - time
        if rest < best_rest[0]:
            best_rest = (rest, bus)
    return best_rest[0] * best_rest[1]


def solve2(data):
    _, busses = parse(data)
    n = step = rest = 1
    bus0 = busses[0]
    while rest < len(busses):
        bus = busses[rest]
        rest += 1
        while bus != 0:
            if ((bus0 * n) + rest - 1) % bus == 0:
                step *= bus
                break
            n += step
    return (n * bus0)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve2(data))
