from functools import reduce
from operator import mul, add
from collections.abc import Callable


class Homework:
    def __init__(self, data: str) -> None:
        self.numbers: list[list[int]] = []
        self.operators: list[Callable[[int, int], int]] = []
        lines = data.strip().split('\n')
        for row in list(zip(*[line.split() for line in lines])):
            self.numbers.append([int(num) for num in row[:-1]])
            self.operators.append(add if row[-1] == '+' else mul)
        self.transposed_all: list[list[str]] = []
        for n in range(len(lines[0])):
            self.transposed_all.append(list(lines[row][-(n + 1)] for row in range(len(lines) - 1)))

    def total(self) -> int:
        return sum(reduce(self.operators[n], row) for n, row in enumerate(self.numbers))

    def total_rl(self) -> int:
        total: int = 0
        pos: int = 0
        for op in reversed(self.operators):
            numbers: list[int] = []
            while pos < len(self.transposed_all):
                number = int(''.join(c.strip() for c in self.transposed_all[pos]) or '0')
                pos += 1
                if not number:
                    break
                numbers.append(number)
            total += reduce(op, numbers)
        return total


def load(data: str) -> Homework:
    return Homework(data)


def solve1(data: str) -> int:
    return load(data).total()


def solve2(data: str) -> int:
    return load(data).total_rl()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
