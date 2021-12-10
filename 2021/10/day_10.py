class Subsystem:
    OPENED = {"<": (25137, 4), "{": (1197, 3), "[": (57, 2), "(": (3, 1)}
    CLOSED = {">": "<", "}": "{", "]": "[", ")": "("}

    def __init__(self, data):
        self.lines = [list(line) for line in data.strip().split("\n")]

    def compile(self):
        errors = dict((par, 0) for par in self.OPENED.keys())
        incompletes = []
        for line in self.lines:
            opened = []
            for par in line:
                if par in self.OPENED:
                    opened.append(par)
                else:
                    par = self.CLOSED[par]
                    if opened.pop() != par:
                        errors[par] += 1
                        break
            else:
                incompletes.append(opened)
        return errors, incompletes

    def sum_errors(self):
        return sum(self.OPENED[error][0] * count for error, count in self.compile()[0].items())

    def complete(self):
        _, incompletes = self.compile()
        points = []
        for opened in incompletes:
            point = 0
            for par in reversed(opened):
                point = point * 5 + self.OPENED[par][1]
            points.append(point)
        points.sort()
        return points[len(points) // 2]


def solve1(data):
    return Subsystem(data).sum_errors()


def solve2(data):
    return Subsystem(data).complete()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
