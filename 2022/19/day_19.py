from collections import deque


def load(data):
    return [[int(s) for s in line.replace(":", " ").split() if s.isdigit()] for line in data.strip().split("\n")]


class Blueprint:
    def __init__(self, data):
        self.robot_costs = [[data[0], 0, 0, 0], [data[1], 0, 0, 0], [data[2], data[3], 0, 0], [data[4], 0, data[5], 0]]

    def best(self, minutes):
        run = deque(((0, [1, 0, 0, 0], [0, 0, 0, 0]),))
        best, seen = 0, {}
        while run:
            minute, robots, minerals = run.popleft()
            print(len(run), minute)
            minute += 1
            buildable_robots = []
            for robot in range(4):
                if all(self.robot_costs[robot][m] <= minerals[m] for m in range(4)):
                    buildable_robots.append(robot)
            collected_minerals = [minerals[n] + robots[n] for n in range(4)]
            if minute == minutes:
                if collected_minerals[3] > best:
                    best = collected_minerals[3]
            else:
                run.append((minute, robots, collected_minerals))
                for robot in buildable_robots:
                    next_robots = robots.copy()
                    next_robots[robot] += 1
                    run.append((minute, next_robots, [minerals[n] - self.robot_costs[robot][n] for n in range(4)]))
        #import pdb; pdb.set_trace()
        return best


class Blueprints:
    def __init__(self, data):
        self.blueprints = {}
        for line in data:
            self.blueprints[line[0]] = Blueprint(line[1:])

    def quality(self, minutes=24):
        return sum(k * blueprint.best(minutes) for k, blueprint in self.blueprints.items())


def solve1(data):
    return Blueprints(load(data)).quality()


def solve2(data):
    return Blueprints(load(data)).quality()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
