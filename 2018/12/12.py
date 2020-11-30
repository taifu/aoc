raw = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""

raw = open("input.txt").read()


def potify(pot):
    return 0 if pot == '.' else 1


def grow(pots, rules):
    pots = (0, 0, 0, 0, 0) + pots[:] + (0, 0, 0, 0, 0)
    next_pots = list(pots)
    for pos in range(len(pots) - 5):
        try:
            next_pots[pos + 2] = rules[tuple(pots[pos:pos + 5])]
        except KeyError:
            next_pots[pos + 2] = 0
            pass
    return tuple(next_pots)


def read(raw):
    rules = {}
    for n, line in enumerate(raw.split("\n")):
        if n == 0:
            pots = tuple(potify(pot) for pot in list(line.split(":")[1].strip()))
        elif n > 1 and line:
            next_pot = potify(line[9])
            if next_pot:
                rules[tuple(potify(pot) for pot in list(line[:5]))] = next_pot
    return pots, rules


def tot(pots, gen):
    return sum((gen * -5 + i) for i, pot in enumerate(pots) if pot)


pots, rules = read(raw)


last_tot, last_diff = 0, None

gen = 0
while True:
    gen += 1
    pots = grow(pots, rules)
    next_tot = tot(pots, gen)
    if gen == 20:
        print(next_tot)
    next_diff = next_tot - last_tot
    if next_diff == last_diff:
        print(next_tot + last_diff * (50000000000 - gen))
        break
    last_tot, last_diff = next_tot, next_diff
