from functools import cache


class Solution:
    def __init__(self, raw: str) -> None:
        parts = raw.strip().split('\n\n')
        self.towels = [towel.strip() for towel in parts[0].split(',')]
        self.patterns = [pattern for pattern in parts[1].split('\n')]

    @cache
    def ways(self, pattern: str) -> int:
        n_ways = 0
        if not pattern:
            return 0
        for towel in self.towels:
            if pattern.startswith(towel):
                n_ways += self.ways(pattern[len(towel):])
        return n_ways

    def count(self) -> int:
        return sum(1 if self.ways(pattern) > 0 else 0 for pattern in self.patterns)

    def count2(self) -> int:
        return sum(self.ways(pattern) for pattern in self.patterns)


def solve1(data: str) -> int:
    return int(Solution(data).count())


def solve2(data: str) -> int:
    return int(Solution(data).count2())


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
