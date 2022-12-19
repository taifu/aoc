from collections import deque


def load(data):
    return [[int(s) for s in line.replace(":", " ").split() if s.isdigit()] for line in data.strip().split("\n")]


class Blueprint:
    def __init__(self, data):
        self.robot_costs = [[data[0], 0, 0, 0], [data[1], 0, 0, 0], [data[2], data[3], 0, 0], [data[4], 0, data[5], 0]]

    def best(self, minutes):
        run = deque(((0, (1, 0, 0, 0), (0, 0, 0, 0)),))
        best, seen = 0, set()
        while run:
            minute, robots, minerals = run.popleft()
            minute += 1
            buildable_robots = []
            for robot in range(4):
                if all(self.robot_costs[robot][m] <= minerals[m] for m in range(4)):
                    buildable_robots.append(robot)
            # Debug
            #print(f"{'  '*minute} Entering {minute} robots={robots} minerals={minerals} buildable_robots={buildable_robots}")
            if minute == minutes:
                if minerals[3] > best:
                    best = minerals[3]
            else:
                if buildable_robots:
                    for robot in buildable_robots:
                        next_robots = tuple(robots[n] + (1 if n == robot else 0) for n in range(4))
                        next_minerals = tuple(minerals[n] - self.robot_costs[robot][n] + robots[n] for n in range(4))
                        if not (minute, next_robots, next_minerals) in seen:
                            seen.add((minute, next_robots, next_minerals))
                            if minute == 7 and next_robots == (1, 3, 0, 0) and next_minerals == (1, 6, 0, 0) :
                                print(f"Found {minute} robots={next_robots} minerals={next_minerals}")
                            elif minute == 11 and next_robots == (1, 3, 1, 0) and next_minerals == (2, 4, 0, 0) :
                                print(f"Found {minute} robots={next_robots} minerals={next_minerals}")
                            elif minute == 12 and next_robots == (1, 4, 1, 0) and next_minerals == (1, 7, 1, 0) :
                                print(f"Found {minute} robots={next_robots} minerals={next_minerals}")
                            elif minute == 15 and next_robots == (1, 4, 2, 0) and next_minerals == (1, 5, 4, 0) :
                                print(f"Found {minute} robots={next_robots} minerals={next_minerals}")
                            elif minute == 18 and next_robots == (1, 4, 2, 1) and next_minerals == (2, 17, 3, 0) :
                                print(f"Found {minute} robots={next_robots} minerals={next_minerals}")
                            elif minute == 21 and next_robots == (1, 4, 2, 2) and next_minerals == (3, 29, 2, 3) :
                                print(f"Found {minute} robots={next_robots} minerals={next_minerals}")
                            elif minute == 23 and next_robots == (1, 4, 2, 2) and next_minerals == (6, 41, 8, 9) :
                                print(f"Found {minute} robots={next_robots} minerals={next_minerals}")
                            #print(f"{'  '*minute}     Exit {minute} robots={next_robots} minerals={next_minerals}")
                            run.append((minute, next_robots, next_minerals))
                minerals = tuple(minerals[n] + robots[n] for n in range(4))
                if not (minute, robots, minerals) in seen:
                    seen.add((minute, robots, minerals))
                    #print(f"{'  '*minute}     Exit {minute} robots={robots} minerals={minerals}")
                    run.append((minute, robots, minerals))
        print(f"Best {best}")
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
