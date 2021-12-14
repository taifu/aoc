class Fold:
    def __init__(self, data):
        dots_lines, folds_lines = [p.strip().split("\n") for p in data.strip().split("\n\n")]
        self.dots = set((tuple(int(p) for p in line.split(","))) for line in dots_lines)
        self.folds = []
        for line in folds_lines:
            parts = line.split("=")
            self.folds.append(int(parts[1]) * (1 if parts[0][-1] == 'x' else -1))

    def folded(self):
        while self.folds:
            self.fold()
        size_x = size_y = 0
        for x, y in self.dots:
            size_x, size_y = max(size_x, x), max(size_y, y)
        folded = "\n"
        for y in range(size_y + 1):
            line = ""
            for x in range(size_x + 1):
                line += '#' if (x, y) in self.dots else '.'
            folded += line + '\n'
        return folded

    def fold(self):
        fold = self.folds.pop(0)
        dots = set()
        for x, y in self.dots:
            if fold > 0:
                if x > fold:
                    x = fold * 2 - x
            elif y > -fold:
                y = -fold * 2 - y
            dots.add((x, y))
        self.dots = dots
        return self


def solve1(data):
    return len(Fold(data).fold().dots)


def solve2(data):
    return Fold(data).folded()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
