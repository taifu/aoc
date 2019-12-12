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
    def energy(self):
        return sum(map(abs, self.positions)) * sum(map(abs, self.velocities))

    def __repr__(self):
        return "Moon {0[0]: >{2}} {0[1]: >{2}} {0[2]: >{2}} {1[0]: >{2}} {1[1]: >{2}} {1[2]: >{2}}".format(self.positions, self.velocities, 8)


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
    def energy(self):
        return sum(moon.energy for moon in self.moons)


if __name__ == "__main__":
    scans = """<x=-3, y=15, z=-11>
<x=3, y=13, z=-19>
<x=-13, y=18, z=-2>
<x=6, y=0, z=-1>"""
    universe = Universe(scans)
    for step in range(1000):
        universe.evolve()
    print(universe.energy)
    universe_start = Universe(scans)
    universe = Universe(scans)
    step = 0
    while True:
        energy = universe.energy
        universe.evolve()
        step += 1
        print("Step {0: >10} {1: >10} {2: >10}".format(step, universe.energy, universe.energy - energy))
