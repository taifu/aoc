from collections import defaultdict


def qty_what(raw):
    n, k = raw.strip().split(" ")
    return int(n.strip()), k.strip().lower()


class Reaction:
    def __init__(self, qty, parts):
        self.qty = qty
        self.needed = [qty_what(part) for part in parts.split(",")]

    def produce(self, qty):
        mult = -(-qty // self.qty)
        return mult * self.qty, [(n * mult, w) for n, w in self.needed]

    @staticmethod
    def elaborate(raw):
        parts, part = raw.split("=>")
        qty, what = qty_what(part)
        return what, Reaction(qty, parts)


def ore_needed(data, fuel_needed):
    reactions = dict((Reaction.elaborate(raw) for raw in data.strip().split("\n")))
    needed = defaultdict(int)
    needed["fuel"] = fuel_needed
    produced = defaultdict(int)
    ore = 0

    while needed:
        now_produced, needed_qty = needed.popitem()
        produced_qty, reactions_used = reactions[now_produced].produce(needed_qty)
        for qty, what in reactions_used:
            if what == "ore":
                ore += qty
                continue
            already = produced.get(what, 0)
            if already < qty:
                used = already
                qty -= already
            else:
                used = qty
                qty = 0
            if qty:
                needed[what] += qty
            if used:
                produced[what] -= used
        produced[now_produced] += produced_qty - needed_qty

    return ore


def test_program_1():
    assert 31 == ore_needed("""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL""")


def test_program_2():
    assert 165 == ore_needed("""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""")


if __name__ == "__main__":
    raw = open("input.txt").read()
    print(ore_needed(raw, 1))
    cargo_ore = 1000000000000
    fuel, step = cargo_ore, cargo_ore
    max_fuel = 0
    while True:
        step //= 2
        if step == 0:
            break
        ore = ore_needed(raw, fuel)
        if ore <= cargo_ore:
            if fuel > max_fuel:
                max_fuel = fuel
            fuel += step
        elif ore > cargo_ore:
            fuel -= step
    print(max_fuel)
