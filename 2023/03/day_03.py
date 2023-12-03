class Schema:
    def __init__(self, data):
        self.map = [list(line) for line in data.strip().split('\n')]
        self.height = len(self.map)
        self.width = len(self.map[0])

    def numbers(self):
        for y in range(self.height):
            x = 0
            while x < self.width:
                number = 0
                while self.map[y][x].isdecimal():
                    number = number * 10 + int(self.map[y][x])
                    x += 1
                    if x == self.width:
                        break
                if number:
                    length = len(str(number))
                    yield length, x - length, y, number
                else:
                    x += 1

    def around(self, x, y, length):
        for d_y in (-1, 0, 1):
            if 0 <= y + d_y < self.height:
                for d_x in range(-1, length + 1, 1 if d_y != 0 else length + 1):
                    if 0 <= x + d_x < self.width:
                        yield self.map[y + d_y][x + d_x], x + d_x, y + d_y

    def sum(self):
        tot = 0
        for length, x, y, number in self.numbers():
            if any(cell != '.' for cell, dx, dy in self.around(x, y, length)):
                tot += number
        return tot

    def gears(self):
        tot = 0
        all_numbers = list(self.numbers())
        for n1, (l1, x1, y1, number1) in enumerate(all_numbers[:-1]):
            for l2, x2, y2, number2 in all_numbers[n1 + 1:]:
                if y2 > y1 + 2:
                    break
                if x2 + l2 > x1 - 2 and x2 < x1 + l1 + 2:
                    for cell, dx1, dy1 in self.around(x1, y1, l1):
                        for _, dx2, dy2 in self.around(x2, y2, l2):
                            if dx1 == dx2 and dy1 == dy2 and cell == '*':
                                tot += number1 * number2
        return tot


def solve1(data):
    return Schema(data).sum()


def solve2(data):
    return Schema(data).gears()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
