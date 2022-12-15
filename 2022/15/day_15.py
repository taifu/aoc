import bisect


def load(data):
    sensors = []
    for line in data.strip().split("\n"):
        parts = line.replace(",", "=").replace(":", "=").split("=")
        sensors.append(tuple(int(parts[n]) for n in (1, 3, 5, 7)))
    return sensors


class Ground:
    def __init__(self, sensors):
        self.sensors = sensors

    def empty_row(self, row):
        empty_zones = []
        for sx, sy, bx, by in self.sensors:
            length = abs(sx - bx) + abs(sy - by) - abs(row - sy)
            if length > 0:
                bisect.insort(empty_zones, (sx - length, sx + length))
        empty = []
        for x1, x2 in empty_zones:
            # First zone
            if not empty:
                empty.append([x1, x2])
            # Extend last
            elif x1 <= empty[-1][1]:
                if x2 > empty[-1][1]:
                    empty[-1][1] = x2
            # Another zone
            elif x1 > empty[-1][1]:
                empty.append([x1, x2])
        return empty

    def beacon(self, row):
        return sum(abs(x2 - x1) for x1, x2 in self.empty_row(row))

    def distress(self, space):
        for row in range(space + 1):
            empty = self.empty_row(row)
            if len(empty) == 2:
                return (empty[0][1] + 1) * 4000000 + row


def solve1(data, row=2000000):
    return Ground(load(data)).beacon(row)

def solve2(data, space=4000000):
    return Ground(load(data)).distress(space)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
