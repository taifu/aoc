from collections import defaultdict


class Lab:
    def __init__(self, data: str) -> None:
        self.splits: dict[int, set[int]] = {}
        for n, line in enumerate(data.strip().splitlines()):
            if n == 0:
                self.start = line.index('S')
            elif n > 1:
                self.splits[n - 2] = set((pos for pos, s in enumerate(line) if s == '^'))
            self.height = n - 1

    def count(self) -> tuple[int, int]:
        tot = 0
        rays = {self.start: 1}
        for h in range(self.height):
            next_rays: dict[int, int] = defaultdict(int)
            for ray, force in rays.items():
                if ray in self.splits[h]:
                    next_rays[ray - 1] += force
                    next_rays[ray + 1] += force
                    tot += 1
                else:
                    next_rays[ray] += force
            rays = next_rays
        return tot, sum(rays.values())


def load(data: str) -> Lab:
    return Lab(data)


def solve1(data: str) -> int:
    return load(data).count()[0]


def solve2(data: str) -> int:
    return load(data).count()[1]


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
