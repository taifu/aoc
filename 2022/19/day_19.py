from collections import deque
from math import prod


def load(data):
    return [[int(s) for s in line.replace(":", " ").split() if s.isdigit()] for line in data.strip().split("\n")]


class Blueprint:
    ORE, CLAY, OBSIDIAN, GEOIDE = (0, 1, 2, 3)

    def __init__(self, data):
        self.id = data[0]
        self.robot_costs = [[data[1], 0, 0, 0], [data[2], 0, 0, 0], [data[3], data[4], 0, 0], [data[5], 0, data[6], 0]]
        self.max_ore = max(cost[self.ORE] for cost in self.robot_costs)

    def best(self, minutes):
        run = deque(((0, (1, 0, 0, 0), (0, 0, 0, 0)),))
        best, seen = 0, set()
        while run:
           minute, robots, minerals = run.popleft()
           if minute == minutes:
                if minerals[self.GEOIDE] > best:
                    best = minerals[self.GEOIDE]
           else:
                minute += 1
                buildable_robots = []
                for robot in range(4):
                    if all(self.robot_costs[robot][m] <= minerals[m] for m in range(4)):
                        buildable_robots.append(robot)
                if self.GEOIDE in buildable_robots:
                    buildable_robots = [self.GEOIDE]
                elif self.OBSIDIAN in buildable_robots:
                    buildable_robots = [self.OBSIDIAN]
                if buildable_robots:
                    for robot in buildable_robots:
                        # Ogni minuto al massimo posso usare self.max_ore, non
                        # ha senso avere più robot-ore
                        if robot == self.ORE and robots[self.ORE] == self.max_ore:
                            continue
                        next_robots = tuple(robots[n] + (1 if n == robot else 0) for n in range(4))
                        next_minerals = tuple(minerals[n] - self.robot_costs[robot][n] + robots[n] for n in range(4))
                        if not (minute, next_robots, next_minerals) in seen:
                            seen.add((minute, next_robots, next_minerals))
                            run.append((minute, next_robots, next_minerals))
                minerals = tuple(minerals[n] + robots[n] for n in range(4))
                if not buildable_robots or minerals[self.ORE] <= self.max_ore:
                    if not (minute, robots, minerals) in seen:
                        seen.add((minute, robots, minerals))
                        run.append((minute, robots, minerals))
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
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
