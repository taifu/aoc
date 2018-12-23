import re

raw = open("input.txt").read()

raw_example = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
"""

raw_example_2 = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
"""


class Bot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __repr__(self):
        return "Bot({},{},{} r:{})".format(self.x, self.y, self.z, self.r)

    def distance(self, x, y, z):
        return abs(self.x - x) + abs(self.y - y) + abs(self.z - z)


class Nanobots:
    def __init__(self, raw):
        self.bots = []
        self.max_bot = None
        for line in raw.strip().split("\n"):
            parts = re.search('^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$', line).groups()
            bot = Bot(*[int(p) for p in parts])
            self.bots.append(bot)
            if self.max_bot is None or self.max_bot.r < bot.r:
                self.max_bot = bot

    def in_range(self):
        found = []
        for bot in self.bots:
            if bot.distance(self.max_bot.x, self.max_bot.y, self.max_bot.z) <= self.max_bot.r:
                found.append(bot)
        return found

    def best_pos(self):
        min_x = min_y = min_z = float("inf")
        max_x = max_y = max_z = float("-inf")
        for bot in self.bots:
            if bot.x < min_x:
                min_x = bot.x
            elif bot.x > max_x:
                max_x = bot.x
            if bot.y < min_y:
                min_y = bot.y
            elif bot.y > max_y:
                max_y = bot.y
            if bot.z < min_z:
                min_z = bot.z
            elif bot.z > max_z:
                max_z = bot.z
        step = max([max_x - min_x, max_y - min_y, max_z - min_z]) // 10
        from_x, to_x = min_x, max_x
        from_y, to_y = min_y, max_y
        from_z, to_z = min_z, max_z
        best_x = best_y = best_z = 0
        while True:
            best_inside = 0
            for x in range(from_x, to_x, step):
                x0 = x + step // 2
                for y in range(from_y, to_y, step):
                    y0 = y + step // 2
                    for z in range(from_z, to_z, step):
                        z0 = z + step // 2
                        inside = 0
                        for bot in self.bots:
                            if bot.distance(x0, y0, z0) < step + bot.r:
                                inside += 1
                        if inside >= best_inside or (inside == best_inside and x + y + z < best_x + best_y + best_z):
                            best_inside = inside
                            best_x, best_y, best_z = x, y, z
            from_x = best_x - step
            from_y = best_y - step
            from_z = best_z - step
            to_x = best_x + step + 1
            to_y = best_y + step + 1
            to_z = best_z + step + 1
            if step == 1:
                break
            step //= 2

        return Bot(0, 0, 0, 0).distance(best_x, best_y, best_z)


# bots = Nanobots(raw_example)
# print(len(bots.in_range()))

# bots = Nanobots(raw_example_2)
# print(bots.best_pos())

bots = Nanobots(raw)
print(len(bots.in_range()))
print(bots.best_pos())
