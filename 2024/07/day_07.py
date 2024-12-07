from typing import TypeAlias, Callable, Any, Optional
from operator import add, mul
from itertools import product


Numbers: TypeAlias = list[int]
Operator: TypeAlias = Callable[[Any, Any], Any]


class Operations:
    def __init__(self, data: str) -> None:
        self.numbers: list[Numbers] = []
        for line in data.splitlines():
            self.numbers.append([int(v) for v in line.replace(':', '').split(' ')])
        self.first_step: Numbers = []

    def conc(self, val1: int, val2: int) -> int:
        return int(val1 * 10**len(str(val2)) + val2)

    def apply(self, values: Numbers, operators: tuple[Operator, ...], target: int) -> int:
        result = values[0]
        for i, op in enumerate(operators):
            result = op(result, values[i + 1])
            if result > target:
                return False
        return result == target

    def check(self, target: int, values: Numbers, operators: tuple[Operator, ...]) -> int:
        for ops in product(operators, repeat=len(values) - 1):
            if self.apply(values, ops, target):
                return True
        return False

    def count(self) -> int:
        total = 0
        for n, values in enumerate(self.numbers):
            if self.check(values[0], values[1:], (add, mul)):
                self.first_step.append(n)
                total += values[0]
        return total

    def count2(self) -> int:
        total = 0
        for n, values in enumerate(self.numbers):
            if n in self.first_step:
                total += values[0]
            elif self.check(values[0], values[1:], (add, mul, self.conc)):
                total += values[0]
        return total


ops: Optional[Operations] = None


def solve1(data: str) -> int:
    global ops
    ops = Operations(data)
    return ops.count()


def solve2(data: str) -> int:
    assert ops
    return ops.count2()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
