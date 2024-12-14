import re
from math import prod
from typing import TypeAlias, List, Tuple, Generator, Set, Optional  # noqa: F401


Claw: TypeAlias = Tuple[int, int, int, int, int, int]


class Robot:
    def __init__(self, x: int, y: int, vx: int, vy: int) -> None:
        self.pos = [x, y]
        self.vel = (vx, vy)

    def move(self, size: Tuple[int, int]) -> None:
        for xy in range(2):
            self.pos[xy] = (self.pos[xy] + self.vel[xy]) % size[xy]


class Solution:
    def __init__(self, data: str, size_x: Optional[int], size_y: Optional[int]) -> None:
        self.robots = []
        for line in data.strip().split('\n'):
            self.robots.append(Robot(*tuple(int(x) for x in re.findall(r"(-?\d+)", line))))
        self.size = (size_x or 101, size_y or 103)

    def safety(self) -> int:
        middle_x = self.size[0] // 2
        middle_y = self.size[1] // 2
        quadrant = [0, 0, 0, 0]
        for robot in self.robots:
            if robot.pos[0] == middle_x or robot.pos[1] == middle_y:
                continue
            n_quadrant = (0 if robot.pos[0] < middle_x else 1) + (2 if robot.pos[1] > middle_y else 0)
            quadrant[n_quadrant] += 1
        return prod(quadrant)

    def draw(self) -> None:
        bath = []
        for y in range(self.size[1]):
            bath.append([0] * self.size[0])
        for robot in self.robots:
            bath[robot.pos[1]][robot.pos[0]] += 1
        print()
        for y in range(self.size[1]):
            line = "".join(str(bath[y][x]) if bath[y][x] > 0 else '.' for x in range(self.size[0]))
            print(line)
        print()

    def count(self) -> int:
        for move in range(100):
            for robot in self.robots:
                robot.move(self.size)
        return self.safety()

    def count2(self) -> int:
        move = 0
        while True:
            for robot in self.robots:
                robot.move(self.size)
            move += 1
            if len(set(tuple(robot.pos) for robot in self.robots)) == len(self.robots):
                self.draw()
                return move


def solve1(data: str, size_x: Optional[int] = None, size_y: Optional[int] = None) -> int:
    solution = Solution(data, size_x, size_y)
    return solution.count()


def solve2(data: str, size_x: Optional[int] = None, size_y: Optional[int] = None) -> int:
    solution = Solution(data, size_x, size_y)
    return solution.count2()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
