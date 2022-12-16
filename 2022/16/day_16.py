from collections import deque, defaultdict
from itertools import combinations


def load(data):
    valves = []
    for line in data.strip().split("\n"):
        parts = line.replace(",", "").replace(";", " ").replace("=", " ").split(" ")
        valves.append([parts[1], int(parts[5]), parts[11:]])
    return valves


class Flow:
    def __init__(self, valves):
        self.start = 'AA'
        self.all_paths(valves)

    def all_paths(self, valves):
        self.pressures = {}
        tubes = defaultdict(list)
        for valve in valves:
            for valve_to in valve[2]:
                tubes[valve[0]].append(valve_to)
                if valve[1]:
                    self.pressures[valve[0]] = valve[1]
        self.paths = {}
        for valve in (self.start,) + tuple(self.pressures):
            queue = deque(((valve, 0),))
            while queue:
                to_valve, dist = queue.popleft()
                if not (valve, to_valve) in self.paths:
                    self.paths[(valve, to_valve)] = dist
                    for next_valve in tubes[to_valve]:
                        if not (valve, next_valve) in self.paths:
                            queue.append((next_valve, dist + 1))

    def flux(self, max_minutes=30, valves_to_open=None):
        if valves_to_open is None:
            valves_to_open = set(self.pressures)
        max_pressure = 0
        # current valve, minutes, pressure, opened valves, to be opened valves
        queue = deque(((self.start, max_minutes, 0, set(), valves_to_open),))
        while queue:
            valve, minutes, pressure, opened, to_open = queue.popleft()
            if pressure > max_pressure:
                max_pressure = pressure
            for next_valve in to_open:
                cost = self.paths[valve, next_valve]
                next_minutes = minutes - cost - 1
                if next_minutes > 0:
                    queue.append((next_valve, next_minutes, pressure + next_minutes * self.pressures[next_valve], opened | {next_valve}, to_open - {next_valve}))
        return max_pressure

    def flux_elephant(self):
        all_valves = set(self.pressures.keys())
        max_pressure = 0
        for my_valves in combinations(all_valves, (len(all_valves) - 1)// 2 + 1):
            my_valves = set(my_valves)
            elephant_valves = all_valves - my_valves
            p1 = self.flux(max_minutes=26, valves_to_open=my_valves)
            p2 = self.flux(max_minutes=26, valves_to_open=elephant_valves)
            pressure = p1 + p2
            if pressure > max_pressure:
                max_pressure = pressure
        return max_pressure


def solve1(data):
    return Flow(load(data)).flux()

def solve2(data):
    return Flow(load(data)).flux_elephant()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
