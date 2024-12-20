from typing import TypeAlias, Dict, List, Tuple, Generator, Set, Optional, Union  # noqa: F401


DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
Position: TypeAlias = Tuple[int, int]
Length: TypeAlias = int


def add_pos(pos: Position, dpos: Position):
    return (pos[0] + dpos[0], pos[1] + dpos[1])


class Solution:
    _instance = None

    @classmethod
    def get_instance(cls, data: str) -> "Solution":
        if cls._instance is None:
            cls._instance = Solution(data)
        return cls._instance

    def __init__(self, raw: str) -> None:
        self.map: Dict[Position, Length] = {}
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

    def find_track(self) -> None:
        length: Length = 0
        pos, visited, self.track = self.start, set((self.start,)), [self.start]
        while pos != self.end:
            for direction in DIRECTIONS:
                next_pos = add_pos(pos, direction)
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

    def count(self, saving: Length = 100, exact: bool = False, cheat_length: Length = 2) -> int:
        total = 0
        for pos in self.track:
            for length in range(2, cheat_length + 1):
                # Manhattan
                for dx in range(-length, length + 1):
                    dy = length - abs(dx)
                    for step in (0, 1):
                        saved = self.map.get(add_pos(pos, (dx, dy)), 0) - self.map[pos] - length
                        if (exact and saved == saving) or (not exact and saved >= saving):
                            total += 1
                        if dy == 0:
                            break
                        dy = -dy
        return total


def solve1(data: str, saving: Length = 100, exact: bool = False) -> int:
    return Solution.get_instance(data).count(saving, exact)


def solve2(data: str, saving: Length = 100, exact: bool = False, cheat_length: Length = 20) -> int:
    return Solution.get_instance(data).count(saving, exact, cheat_length)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
