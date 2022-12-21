from collections import defaultdict
from operator import add, sub, mul, truediv


def load(data):
    Monkey.reset()
    for line in data.strip().split("\n"):
        Monkey(line.replace(":", "").split(" "))


class Monkey:
    @staticmethod
    def reset():
        Monkey.all_monkeys = {}
        Monkey.yelling = set()
        Monkey.waited_from = defaultdict(list)

    def __init__(self, parts):
        self.name = parts[0]
        Monkey.all_monkeys[self.name] = self
        if parts[1].isdigit():
            self.value = int(parts[1])
            Monkey.yelling.add(self)
        else:
            self.operator = {'*': mul, '/': truediv, '+': add, '-': sub}[parts[2]]
            self.values = [None, None]
            self.order = (parts[1], parts[3])
            self.waiting = set([parts[1], parts[3]])
            Monkey.waited_from[parts[1]].append(self.name)
            Monkey.waited_from[parts[3]].append(self.name)


def root(data, both=False):
    load(data)
    while True:
        for monkey in Monkey.yelling.copy():
            for waiting_name in Monkey.waited_from.pop(monkey.name):
                monkey_waiting = Monkey.all_monkeys[waiting_name]
                monkey_waiting.values[monkey_waiting.order.index(monkey.name)] = monkey.value
                monkey_waiting.waiting.remove(monkey.name)
                if not monkey_waiting.waiting:
                    monkey_waiting.value = monkey_waiting.operator(*monkey_waiting.values)
                    if monkey_waiting.name == 'root':
                        if both:
                            # For part 2
                            return monkey_waiting.values
                        return monkey_waiting.value
                    Monkey.yelling.add(monkey_waiting)
            Monkey.yelling.remove(monkey)


def replace(data, name, value):
    return '\n'.join(f"{name}: {value}" if line[:4] == name else line for line in data.split('\n'))


def brute_force(data):
    my_name = 'humn'
    # Find which value is fixed
    values_zero = root(replace(data, my_name, 0), True)
    values_one = root(replace(data, my_name, 1), True)
    fixed_index = 0 if values_zero[0] == values_one[0] else 1
    inc = value = 1
    # Find initial slope
    check = (lambda x, y: x < y) if values_one[1 - fixed_index] > values_zero[1 - fixed_index] else (lambda x, y: x > y)
    while True:
        new_values = root(replace(data, my_name, value), True)
        if new_values[1 - fixed_index] == new_values[fixed_index]:
            return value
        elif check(new_values[1 - fixed_index], new_values[fixed_index]):
            inc *= 2
            value += inc
        else:
            inc //= 2
            value -= inc


def solve1(data):
    return int(root(data))


def solve2(data):
    return brute_force(data)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
