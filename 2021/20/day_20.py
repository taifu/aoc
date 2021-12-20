import itertools


class Image:
    def __init__(self, data):
        parts = data.strip('\n').split('\n\n')
        self.algo = tuple(c == '#' for c in "".join(parts[0].split('\n')))
        raw = parts[1].split('\n')
        self.image = dict(((x, y), c == '#') for y, line in enumerate(raw) for x, c in enumerate(line))
        self.start = 0
        self.size_x, self.size_y = len(raw[0]), len(raw)

    def draw(self):
        print()
        for y in range(self.start, self.start + self.size_y + 1):
            line = ""
            for x in range(self.start, self.start + self.size_x + 1):
                line += '#' if self.image.get((x, y), 0) else '.'
            print(line)

    def around(self, x, y, outside):
        n = 0
        for dy in (y - 1, y, y + 1):
            for dx in (x - 1, x, x + 1):
                n = n * 2 + self.image.get((dx, dy), outside)
        return n

    def enhance(self, times, drawing=False):
        outside = 0
        for n in range(times):
            if drawing:
                self.draw()
            self.start -= 2
            self.size_x += 4
            self.size_y += 4
            image = {}
            self.lit = 0
            for y in range(self.start, self.start + self.size_y + 1):
                for x in range(self.start, self.start + self.size_x + 1):
                    n = self.around(x, y, outside)
                    pixel = self.algo[n]
                    if pixel:
                        self.lit += 1
                    image[x, y] = pixel
            outside = self.algo[511 if outside else 0]
            self.image = image
        if drawing:
            self.draw()


def solve1(data):
    image = Image(data)
    image.enhance(2)
    return image.lit


def solve2(data):
    image = Image(data)
    image.enhance(50)
    return image.lit


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
