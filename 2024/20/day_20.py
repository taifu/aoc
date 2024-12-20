from typing import TypeAlias, Dict, List, Tuple, Generator, Set, Optional, Union  # noqa: F401


DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
Position: TypeAlias = Tuple[int, int]


class Solution:
    _instance = None

    @classmethod
    def get_instance(cls, data: str) -> "Solution":
        if cls._instance is None:
            cls._instance = Solution(data)
        return cls._instance

    def __init__(self, raw: str) -> None:
        self.map = {}
        for y, line in enumerate(raw.strip().splitlines()):
            for x, char in enumerate(line):
                if char != '#':
                    self.map[x, y] = 0
                    if char == 'S':
                        self.start = (x, y)
                    elif char == 'E':
                        self.end = (x, y)
        self.size = len(line)
        self.find_track()

    def find_track(self):
        length = 0
        pos, visited, self.track = self.start, set((self.start,)), [self.start]
        while pos != self.end:
            for direction in DIRECTIONS:
                next_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if next_pos in visited:
                    continue
                visited.add(next_pos)
                if next_pos in self.map:
                    pos, length = next_pos, length + 1
                    self.map[pos] = length
                    self.track.append(pos)
                    break
            else:
                assert False

    def draw(self, cheats: Tuple[Position, ...] = ()) -> None:
        print()
        for y in range(self.size):
            line = ""
            for x in range(self.size):
                if (x, y) in cheats:
                    line += "o"
                elif (x, y) in self.map:
                    line += "."
                else:
                    line += "#"
            print(line)
        print()

    def count(self, saving: int = 100, exact: bool = False, cheat_length: int = 2) -> int:
        total = 0
        for pos in self.track:
            for length in range(2, cheat_length + 1):
                # Manhattan
                for dx in range(-length, length + 1):
                    dy = length - abs(dx)
                    for step in (0, 1):
                        cheat = (pos[0] + dx, pos[1] + dy)
                        saved = self.map.get(cheat, 0) - self.map[pos] - length
                        if (exact and saved == saving) or (not exact and saved >= saving):
                            total += 1
                        if dy == 0:
                            break
                        dy = -dy
        return total


def solve1(data: str, saving=100, exact=False) -> int:
    return Solution.get_instance(data).count(saving, exact)


def solve2(data: str, saving=100, exact=False, cheat_length=20) -> int:
    return Solution.get_instance(data).count(saving, exact, cheat_length)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))