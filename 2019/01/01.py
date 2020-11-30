def fuel(mass):
    return mass // 3 - 2


def fuel_inc(mass):
    tot_fuel, add_fuel = 0, mass
    while True:
        add_fuel = fuel(add_fuel)
        if add_fuel <= 0:
            return tot_fuel
        tot_fuel += add_fuel


def fuel_rec(mass):
    new_fuel = mass // 3 - 2
    return new_fuel + fuel_rec(new_fuel) if new_fuel > 0 else 0


assert(fuel(12) == 2)
assert(fuel(14) == 2)
assert(fuel(1969) == 654)
assert(fuel(100756) == 33583)

print(sum(fuel(int(mass.strip())) for mass in open("input.txt").readlines()))

assert(fuel_inc(14) == 2)
assert(fuel_inc(1969) == 966)
assert(fuel_inc(100756) == 50346)

print(sum(fuel_inc(int(mass.strip())) for mass in open("input.txt").readlines()))
