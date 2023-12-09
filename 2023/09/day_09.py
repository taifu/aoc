from dataclasses import dataclass


@dataclass
class Sequence:
    numbers: list[int]

    def next(self) -> list[int]:
        diffs = [self.numbers[:]]
        while len(set(diffs[-1])) > 1:
            diffs.append(list(diffs[-1][n] - diffs[-1][n - 1] for n in range(1, len(diffs[-1]))))
        for n in range(len(diffs) - 2, -1, -1):
            for pos, ins, op in ((0, 0, int.__sub__), (-1, len(diffs[n]) + 1, int.__add__)):
                diffs[n].insert(ins, op(diffs[n][pos], diffs[n + 1][pos]))
        return diffs[0]


class Sequences:
    def __init__(self, data: str):
        self.sequences = [Sequence(list(int(n) for n in line.split())) for line in data.splitlines()]

    def total(self, part2: bool = False) -> int:
        return sum(sequence.next()[0 if part2 else -1] for sequence in self.sequences)


def solve1(data: str) -> int:
    return Sequences(data).total()


def solve2(data: str) -> int:
    return Sequences(data).total(True)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
