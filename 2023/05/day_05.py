from typing import TypeAlias, List

Mapping: TypeAlias = List[List[int]]


class Almanac(object):
    def __init__(self, data: str):
        parts = data.strip().split('\n\n')
        self.seeds = [int(n) for n in parts[0].split(':')[1].strip().split()]
        self.mappings: List[Mapping] = []
        for part in parts[1:]:
            feature = []
            for coords in part.split(':')[1].strip().split('\n'):
                feature.append([int(n) for n in coords.split()])
            ranges = sorted(feature, key=lambda f: f[1])
            if ranges[0][1] != 0:
                mapping = [[0, ranges[0][1] - 1, 0]]
            else:
                mapping = []
            for n, range_ in enumerate(ranges):
                mapping.append([range_[1], range_[1] + range_[2] - 1, range_[0] - range_[1]])
            self.mappings.append(mapping)
        # Fill mappings holes
        for mapping in self.mappings:
            n = 0
            while n < len(mapping) - 1:
                if mapping[n][1] != mapping[n + 1][0] - 1:
                    mapping.insert(n + 1, [mapping[n][1] + 1, mapping[n + 1][0] - 1, 0])
                    n += 1
                n += 1
        starts = set([start for start, _, _ in self.mappings[-1]])
        for mapping in self.mappings[::-1][1:]:
            starts = set([self.find(mapping, start, reverse=True) for start in starts])
            for start, _, _ in mapping:
                starts.add(start)
        # Find all intervals
        intervals = [[0, self.jump(0)]]
        for n, check in enumerate(sorted(starts)):
            gap = self.jump(check) - check
            if gap != intervals[-1][1]:
                intervals.append([check, gap])
        self.intervals = [[gap[0], (intervals + [[10**20]])[n + 1][0] - 1, gap[1]] for n, gap in enumerate(intervals)]

    def find(self, mapping: Mapping, jump: int, reverse: bool = False) -> int:
        if reverse:
            mapping = sorted([[a + c, b + c, -c] for a, b, c in mapping])
        if jump > mapping[-1][1]:
            return jump
        start = step = len(mapping) // 2
        while True:
            if jump >= mapping[start][0] and jump <= mapping[start][1]:
                return jump + mapping[start][2]
            if step not in (1, -1):
                step //= 2
            if jump < mapping[start][0]:
                start -= step
            else:
                start += step

    def jump(self, start: int) -> int:
        for mapping in self.mappings:
            start = self.find(mapping, start)
        return start

    def lowest(self) -> int:
        return min(self.jump(seed) for seed in self.seeds)

    def lowest2(self) -> int:
        lowest = 10**20
        for seed_start, seed_delta in zip(self.seeds[::2], self.seeds[1::2]):
            seed_end = seed_start + seed_delta - 1
            for start, end, gap in self.intervals:
                if not (seed_start > end or seed_end < start):
                    lowest = min(lowest, self.jump(max(seed_start, start)), self.jump(min(seed_end, end)))
        return lowest


def solve1(data: str) -> int:
    return Almanac(data).lowest()


def solve2(data: str) -> int:
    return Almanac(data).lowest2()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
