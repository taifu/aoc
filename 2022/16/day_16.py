from collections import deque, defaultdict
from itertools import combinations


def load(data):
    valves = []
    for line in data.strip().split("\n"):
        parts = line.replace(",", "").replace(";", " ").replace("=", " ").split(" ")
        valves.append([parts[1], int(parts[5]), parts[11:]])
    return valves


class Flow:
    def __init__(self, valves, start='AA'):
        self.start = start
        self.valves = valves
        self.tubes = {}
        self.pressures = {}
        self.times = {}
        for valve in valves:
            self.tubes[valve[0]] = valve[2]
            for next_valve in valve[2]:
                self.times[(valve[0], next_valve)] = 1
            self.tubes[valve[0]] = valve[2]
            if valve[1]:
                self.pressures[valve[0]] = valve[1]
        self.all_paths()
        for valve, paths in self.paths.items():
            self.paths[valve] = [(next_valve, cost) for (next_valve, cost) in paths]
            assert(self.paths[valve])

    def calc_path(self, valve_start, valve_end, visited):
        #print("enter", valve_start, valve_end, visited)
        #if valve_start == 'JJ' and valve_end == 'EE':
            #import pdb; pdb.set_trace()
        try:
            ret = self.times[(valve_start, valve_end)]
            #print("exit", valve_start, valve_end, ret)
            return ret
        except KeyError:
            min_weight = None
            for next_valve in self.tubes[valve_start]:
                if next_valve not in visited:
                    weight = self.calc_path(next_valve, valve_end, visited.union({valve_start}))
                    if weight is not None and (min_weight is None or weight < min_weight):
                        min_weight = weight
            if min_weight is None:
                return None
                #import pdb; pdb.set_trace()
                #self.times[(valve_start, valve_end)] = inf
                #return inf
            #print("exit", valve_start, valve_end, 1 + min_weight)
            self.times[(valve_start, valve_end)] = 1 + min_weight
            return 1 + min_weight

    def all_paths(self):
        self.paths = defaultdict(list)
        for pressured_valve in self.pressures.keys():
            self.paths[self.start].append((pressured_valve, self.calc_path(self.start, pressured_valve, {self.start})))
            for pressured_valve_2 in self.pressures.keys():
                if pressured_valve_2 != pressured_valve:
                    self.paths[pressured_valve].append((pressured_valve_2, self.calc_path(pressured_valve, pressured_valve_2, {pressured_valve})))

    def flux(self, max_minutes=30, valves_to_open=None):
        # Valve, minutes, pressure, opened
        queue = deque((('AA', 1, 0, []),))
        max_pressure = 0
        while queue:
            valve, minutes, pressure, opened = queue.pop()
            if pressure > max_pressure:
                max_pressure = pressure
            for next_valve, cost in self.paths[valve]:
                if minutes + cost < max_minutes:
                    if (valves_to_open is None or next_valve in valves_to_open) and next_valve not in opened:
                        queue.append((next_valve, minutes + cost + 1, pressure + (max_minutes - cost - minutes) * self.pressures[next_valve], opened + [next_valve]))
        return max_pressure

    def flux2(self):
        all_valves = set(self.pressures.keys())
        max_pressure = 0
        for n_my_valves in range((len(all_valves) - 1)// 2 + 1, len(all_valves)):
            #if n_my_valves == 9:
                #import pdb; pdb.set_trace()
            for my_valves in combinations(all_valves, n_my_valves):
                elephant_valves = tuple(all_valves - set(my_valves))
                #if my_valves == set(('DC', 'IV', 'QB', 'QR', 'SB', 'UE', 'VK', 'XK', 'ZE')):
                    #import pdb; pdb.set_trace()
                p1 = self.flux(max_minutes=26, valves_to_open=my_valves)
                p2 = self.flux(max_minutes=26, valves_to_open=elephant_valves)
                pressure = p1 + p2
                if pressure > max_pressure:
                    print(p1, p2)
                    print(my_valves, elephant_valves)
                    max_pressure = pressure
        return max_pressure


def solve1(data):
    return Flow(load(data)).flux()

def solve2(data):
    return Flow(load(data)).flux2()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
