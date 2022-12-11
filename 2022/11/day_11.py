from operator import mul, add
from math import prod


class Monkey:
    def _operation(self, line):
        parts = line.split()
        operator = {"*": mul, "+": add}[parts[1]]
        if parts[0] == parts[2] == "old":
            return lambda old: operator(old, old)
        elif parts[0] == "old":
            return lambda old: operator(old, int(parts[2]))
        elif parts[2] == "old":
            return lambda old: operator(int(parts[0]), old)
        else:
            return lambda old: operator(int(parts[0]), int(parts[2]))

    def __init__(self, lines):
        self.inspected = 0
        self.number = int(lines[0].split()[1][:-1])
        self.items = [int(item.strip()) for item in lines[1].split(":")[1].split(",")]
        self.operation = self._operation(lines[2].split("=")[1].strip())
        self.divisible = int(lines[3].split(" ")[-1])
        self.results = [int(line.split()[-1]) for line in lines[5:3:-1]]

    def turn(self, monkeys, divided, divisibility):
        while self.items:
            self.inspected += 1
            item = (self.operation(self.items.pop()) // divided) % divisibility
            monkeys[self.results[item % self.divisible == 0]].items.append(item)


def load(data):
    monkeys = []
    for lines in data.strip().split("\n\n"):
        monkeys.append(Monkey(lines.split("\n")))
    return monkeys


def compute(monkeys, turns=20, divided=3):
    divisibility = prod([m.divisible for m in monkeys])
    for turn in range(turns):
        for monkey in monkeys:
            monkey.turn(monkeys, divided, divisibility)
    return mul(*[m.inspected for m in sorted(monkeys, key=lambda m: m.inspected)[-2:]])


def solve1(data):
    return compute(load(data))


def solve2(data):
    return compute(load(data), 10000, 1)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
