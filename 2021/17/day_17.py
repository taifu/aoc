class Trench:
    cache = {}

    def __init__(self, data):
        target_x = tuple(int(p) for p in data.split("x=")[1].split(",")[0].split(".."))
        target_y = tuple(int(p) for p in data.split("y=")[-1].split(".."))
        self.target = (target_x, target_y)

    def probe(self, vel_x, vel_y):
        x, y, max_y = 0, 0, 0
        while True:
            if x > self.target[0][1] or -y > -self.target[1][0]:
                return None
            if x >= self.target[0][0] and -y >= -self.target[1][1]:
                return max_y
            x, vel_x = x + vel_x, max(0, vel_x - 1)
            y, vel_y = y + vel_y, vel_y - 1
            if y > max_y:
                max_y = y

    def highest(self):
        try:
            return Trench.cache[self.target]
        except KeyError:
            pass
        max_max_y, max_val, cont = 0, 200, 0
        for vel_x in range(1, max_val):
            for vel_y in range(-max_val, max_val):
                if (max_y := self.probe(vel_x, vel_y)) is not None:
                    cont += 1
                if max_y is not None and max_y > max_max_y:
                    max_max_y = max_y
        Trench.cache[self.target] = max_max_y, cont
        return max_max_y, cont


def solve1(data):
    return Trench(data).highest()[0]


def solve2(data):
    return Trench(data).highest()[1]


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
