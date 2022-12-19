from collections import deque
from math import prod


def load(data):
    return [[int(s) for s in line.replace(":", " ").split() if s.isdigit()] for line in data.strip().split("\n")]


class Blueprint:
    ORE, CLAY, OBSIDIAN, GEOIDE = (0, 1, 2, 3)

    def __init__(self, data):
        self.id = data[0]
        self.robot_costs = [[data[1], 0, 0, 0], [data[2], 0, 0, 0], [data[3], data[4], 0, 0], [data[5], 0, data[6], 0]]
        self.max_costs = [max(cost[n] for cost in self.robot_costs) for n in range(4)]
        self.max_costs[self.GEOIDE] = 9999

    def useless(self, max_minutes, minutes, best, robots, minerals):
        # Non ha senso seguire un ramo in cui anche al meglio non si potrà
        # superare la miglior soluzione attuale
        # costruzione del robot più costoso sommato alla produzione dei robot
        if minerals[self.GEOIDE] + (max_minutes**2 - minutes**2) // 2 * (1 + robots[self.GEOIDE]) <= best:
            return True
        return False

    def limit_mineral(self, robots, minerals):
        # Non ha senso avere più minerali rispetto a quelli che servono per la
        # costruzione del robot più costoso sommato alla produzione dei robot
        return tuple(min(mineral, self.max_costs[n] + robots[n]) for n, mineral in enumerate(minerals))

    def best(self, max_minutes):
        run = deque(((0, (1, 0, 0, 0), (0, 0, 0, 0)),))
        best, seen = 0, set()
        while run:
           minutes, robots, minerals = run.popleft()
           if minutes == max_minutes:
                if minerals[self.GEOIDE] > best:
                    best = minerals[self.GEOIDE]
           else:
                minutes += 1
                buildable_robots = []
                for robot in range(4):
                    if all(self.robot_costs[robot][m] <= minerals[m] for m in range(4)):
                        buildable_robots.append(robot)
                if self.GEOIDE in buildable_robots:
                    buildable_robots = [self.GEOIDE]
                if buildable_robots:
                    for robot in buildable_robots:
                        # Ogni minuto al massimo posso usare self.max_costs, non
                        # ha senso avere più robot di questo tipo
                        if robots[robot] == self.max_costs[robot] and robot != self.GEOIDE:
                            continue
                        next_robots = tuple(robots[n] + (1 if n == robot else 0) for n in range(4))
                        next_minerals = self.limit_mineral(next_robots, (minerals[n] - self.robot_costs[robot][n] + robots[n] for n in range(4)))
                        if not (minutes, next_robots, next_minerals) in seen:
                            seen.add((minutes, next_robots, next_minerals))
                            if not self.useless(max_minutes, minutes, best, next_robots, minerals):
                                run.append((minutes, next_robots, next_minerals))
                minerals = self.limit_mineral(robots, (minerals[n] + robots[n] for n in range(4)))
                if not (minutes, robots, minerals) in seen:
                    seen.add((minutes, robots, minerals))
                    if not self.useless(max_minutes, minutes, best, robots, minerals):
                        run.append((minutes, robots, minerals))
        return best


class Blueprints:
    def __init__(self, data):
        self.blueprints = []
        for line in data:
            self.blueprints.append(Blueprint(line))

    def quality(self):
        return sum(blueprint.id * blueprint.best(24) for blueprint in self.blueprints)

    def quality2(self):
        return prod(blueprint.best(32) for blueprint in self.blueprints[:3])


def solve1(data):
    return Blueprints(load(data)).quality()


def solve2(data):
    return Blueprints(load(data)).quality2()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
