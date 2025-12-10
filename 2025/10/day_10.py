from itertools import combinations
from functools import reduce
from operator import xor


class Machine:
    def __init__(self, line: str) -> None:
        parts = line.replace('{', ']').split(']')
        self.size = len(parts[0]) - 1
        self.target = int(parts[0][1:].replace('#', '1').replace('.', '0')[::-1], 2)
        self.buttons = [sum(2**int(n) for n in but.split(',')) for but in parts[1].replace(' ', '').replace('(', '').strip(')').split(')')]
        self.joltage = [int(p) for p in parts[2][:-1].split(',')]

    def switch_on(self):
        for cont in range(1, len(self.buttons) + 1):
            for used in combinations(self.buttons, cont):
                if reduce(xor, used) == self.target:
                    return cont
        assert False


class Factory:
    def __init__(self, data: str) -> None:
        self.machines = [Machine(line) for line in data.strip().splitlines()]

    def switch_on(self) -> int:
        return sum(machine.switch_on() for machine in self.machines)


def load(data: str) -> Factory:
    return Factory(data)


def solve1(data: str) -> int:
    return load(data).switch_on()


def solve2(data: str) -> int:
    return load(data).switch_on()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
