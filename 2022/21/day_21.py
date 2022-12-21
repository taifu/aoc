from collections import defaultdict
from operator import add, sub, mul, floordiv


def load(data):
    Monkey.reset()
    for line in data.strip().split("\n"):
        Monkey(line.replace(":", "").split(" "))


class Monkey:
    @staticmethod
    def reset():
        Monkey.monkeys = {}
        Monkey.waiting = {}
        Monkey.yelling = set()
        Monkey.waited_from = defaultdict(list)

    def __init__(self, parts):
        self.name = parts[0]
        Monkey.monkeys[self.name] = self
        if parts[1].isdigit():
            self.value = int(parts[1])
            Monkey.yelling.add(self)
        else:
            self.operator = {'*': mul, '/': floordiv, '+': add, '-': sub}[parts[2]]
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
                monkey_waiting = Monkey.monkeys[waiting_name]
                index = monkey_waiting.order.index(monkey.name)
                monkey_waiting.values[index] = monkey.value
                monkey_waiting.waiting.remove(monkey.name)
                if not monkey_waiting.waiting:
                    monkey_waiting.value = monkey_waiting.operator(*monkey_waiting.values)
                    if monkey_waiting.name == 'root':
                        if both:
                            return monkey_waiting.values
                        return monkey_waiting.value
                    Monkey.yelling.add(monkey_waiting)
            Monkey.yelling.remove(monkey)


def replace(data, name, value):
    return '\n'.join(f"{name}: {value}" if line[:4] == name else line for line in data.split('\n'))


def brute_force(data):
    # Root values for root
    my_name = 'humn'
    values = root(data, True)
    values_post = root(replace(data, my_name, 0), True)
    index = 1 if values_post[0] == values[0] else 0
    value = inc = 1
    while True:
        new_values = root(replace(data, my_name, value), True)
        print(new_values)
        if new_values[index] > new_values[1 - index]:
            inc *= 2
            value += inc
        elif new_values[index] < new_values[1 - index]:
            inc //= 2
            value -= inc
        else:
            return value


def solve1(data):
    return root(data)


def solve2(data):
    return brute_force(data)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
