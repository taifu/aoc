class Range:
    def __init__(self, line: str):
        self.start, self.end = [int(p) for p in line.split('-')]

    def __repr__(self):
        return f"{self.start}-{self.end}"


def invalids(start: int, end: int, part: int = 1):
    found = set()
    for step in range(1, len(str(end)) // 2 + 1):
        for rep in range(max(2, len(str(start)) // step), len(str(end)) // step + 1):
            if part == 1 and rep != 2:
                continue
            block = step
            while True:
                if (invalid := int(str(block) * rep)) > end:
                    break
                if invalid >= start and invalid not in found:
                    found.add(invalid)
                    yield invalid
                if len(str(block := block + 1)) > step:
                    break


def load(data: str) -> (Range, ...):
    return tuple(Range(line) for line in data.strip().split(','))


def count(ranges: (Range, ...)) -> int:
    return sum(invalid for range in ranges for invalid in invalids(range.start, range.end))


def count2(ranges: (Range, ...)) -> int:
    return sum(invalid for range in ranges for invalid in invalids(range.start, range.end, part=2))


def solve1(data: str) -> int:
    return count(load(data))


def solve2(data: str) -> int:
    return count2(load(data))


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
