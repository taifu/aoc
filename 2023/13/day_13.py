class Pattern:
    def __init__(self, raw: str):
        self.map = [list(line) for line in raw.splitlines()]
        self.height, self.width = len(self.map), len(self.map[0])

    def getter(self, col: bool, f: int, s: int) -> str:
        return self.map[f][s] if col else self.map[s][f]

    def reflection(self, col: bool = True, part2: bool = False) -> int:
        if col:
            max_first, max_second = self.width, self.height
        else:
            max_first, max_second = self.height, self.width
        for first in range(max_first - 1):
            bad, to = 0, -1
            if first >= max_first // 2:
                to = (first - max_first // 2) * 2
            for second in range(max_second):
                for delta, check in enumerate(range(first, to, -1)):
                    if self.getter(col, second, check) != self.getter(col, second, check + 1 + delta * 2):
                        bad += 1
            if bad == 0 and not part2 or bad == 1 and part2:
                return first + 1
        return 0


def solve1(data: str, part2: bool = False) -> int:
    return sum(pattern.reflection(col=True, part2=part2) + 100 * pattern.reflection(col=False, part2=part2)
               for pattern in [Pattern(raw) for raw in data.strip().split('\n\n')])


def solve2(data: str) -> int:
    return solve1(data, True)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
