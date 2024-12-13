import re
from typing import TypeAlias, List, Tuple, Generator, Set  # noqa: F401


Claw: TypeAlias = Tuple[int, int, int, int, int, int]


class Solution:
    def __init__(self, data: str) -> None:
        self.claws = []
        for line in data.strip().split('\n\n'):
            # Ax Ay Bx By X Y
            self.claws.append(tuple(int(x) for x in re.findall(r"(\d+)", line)))

    def count(self, factor: int = 0) -> int:
        total = 0
        for Ax, Ay, Bx, By, X, Y in self.claws:
            det = Ax * By - Ay * Bx
            assert det != 0
            det_x, det_y = (X + factor) * By - (Y + factor) * Bx, (Y + factor) * Ax - (X + factor) * Ay
            tokenA, tokenB = det_x / det, det_y / det
            if float(tokenA).is_integer() and float(tokenB).is_integer():
                total += int(tokenA) * 3 + int(tokenB)
        return total

    def count2(self) -> int:
        return self.count(10000000000000)


solution = None


def solve1(data: str) -> int:
    global solution
    solution = Solution(data)
    return solution.count()


def solve2(data: str) -> int:
    assert solution
    return solution.count2()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
