type Battery = tuple[int, ...]
type Batteries = tuple[Battery, ...]


def load(data: str) -> Batteries:
    return tuple(tuple(int(c) for c in line) for line in data.strip().splitlines())


def best(battery: Battery, length: int) -> int:
    if length == 1:
        return max(battery)
    max_digit = max(battery[:1 - length])
    return 10**(length - 1) * max_digit + best(battery[battery.index(max_digit) + 1:], length - 1)


def count(batteries: Batteries, length: int = 2) -> int:
    return sum(best(battery, length) for battery in batteries)


def solve1(data: str) -> int:
    return count(load(data))


def solve2(data: str) -> int:
    return count(load(data), 12)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
