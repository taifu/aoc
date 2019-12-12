import functools


# This function computes GCD
def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


# This function computes LCM
def lcm(x, y):
    lcm = (x * y) // gcd(x, y)
    return lcm


class Moon:
    def __init__(self, scan):
        self.positions = [int(part.split("=")[1]) for part in scan[1:-1].split(",")]
        self.velocities = [0 for n in range(len(self.positions))]

    def update_velocities(self, moon):
        for n, position in enumerate(self.positions):
            if position > moon.positions[n]:
                delta = 1
            elif position < moon.positions[n]:
                delta = -1
            else:
                delta = 0
            if delta:
                self.velocities[n] -= delta
                moon.velocities[n] += delta

    def update_positions(self):
        for n in range(len(self.positions)):
            self.positions[n] += self.velocities[n]

    @property
    def abs_pos(self):
        return sum(map(abs, self.positions))

    @property
    def abs_vel(self):
        return sum(map(abs, self.velocities))

    @property
    def energy(self):
        return self.abs_pos * self.abs_vel

    def __eq__(self, other):
        return all(v1 == v2 for v1, v2 in zip(*[[v for s in [getattr(m, k) for k in ('positions', 'velocities')] for v in s] for m in (self, other)]))

    def same_axis(self, other, axis):
        return all(v1 == v2 for v1, v2 in zip(*[[getattr(m, k)[axis] for k in ('positions', 'velocities')] for m in (self, other)]))

    def __repr__(self):
        return "Moon {0[0]: >{2}} {0[1]: >{2}} {0[2]: >{2}} {1[0]: >{2}} {1[1]: >{2}} {1[2]: >{2}}".format(self.positions, self.velocities, 5)


class Universe:
    def __init__(self, scans):
        self.moons = [Moon(scan) for scan in scans.split("\n")]

    def evolve(self):
        for n, moon1 in enumerate(self.moons[:-1]):
            for moon2 in self.moons[n + 1:]:
                moon1.update_velocities(moon2)
        for moon in self.moons:
            moon.update_positions()

    @property
    def abs_pos(self):
        return sum(moon.abs_pos for moon in self.moons)

    @property
    def abs_vel(self):
        return sum(moon.abs_vel for moon in self.moons)

    @property
    def energy(self):
        return sum(moon.energy for moon in self.moons)

    def __repr__(self):
        return " ".join(repr(moon) for moon in self.moons)


if __name__ == "__main__":
    scans = open("input.txt").read().strip()
    universe = Universe(scans)
    for step in range(1000):
        universe.evolve()
    print(universe.energy)
    universe_start = Universe(scans)
    universe = Universe(scans)
    step = 0
    AXIS = list(range(len(universe_start.moons[0].positions)))
    LOOPS = [None for n in AXIS]
    while True:
        abs_pos, abs_vel = universe.abs_pos, universe.abs_vel
        universe.evolve()
        step += 1
        for axis in AXIS:
            if LOOPS[axis]:
                continue
            for n, moon in enumerate(universe.moons):
                if not moon.same_axis(universe_start.moons[n], axis):
                    break
            else:
                LOOPS[axis] = step
        if all(LOOPS):
            break
    print(functools.reduce(lcm, LOOPS))
