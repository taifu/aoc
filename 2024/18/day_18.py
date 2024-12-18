import heapq
from typing import TypeAlias, Dict, List, Tuple, Generator, Set, Optional, Union  # noqa: F401

Position: TypeAlias = Tuple[int, int]
Direction: TypeAlias = Tuple[int, int]

E, S, W, N = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIRECTIONS = (E, S, W, N)
BYTE = '#'


class Solution:
    def __init__(self, raw: str, how_many: int, size: int) -> None:
        self.map = {}
        self.start = (0, 0)
        self.size = size + 1
        self.end = (size, size)
        self.bytes = []
        for n, line in enumerate(raw.strip().splitlines()):
            if n >= how_many:
                break
            x, y = [int(c) for c in line.split(',')]
            self.bytes.append((x, y))
            self.map[x, y] = BYTE

    def draw(self, visited: Set[Position]) -> None:
        print()
        for y in range(self.size):
            line = ""
            for x in range(self.size):
                if self.map.get((x, y)) == BYTE:
                    line += BYTE
                elif (x, y) in visited:
                    line += 'O'
                else:
                    line += "."
            print(line)
        print()

    def explore(self) -> Union[int, float]:
        stack: List[Tuple[int, Position]] = []
        heapq.heappush(stack, (0, self.start))
        self.visited: Dict[Position, int] = {}

        while stack:
            length, pos = heapq.heappop(stack)
            try:
                if self.visited[pos] < length:
                    continue
            except KeyError:
                pass

            for dx, dy in DIRECTIONS:
                next_pos = (pos[0] + dx, pos[1] + dy)
                if next_pos[0] < 0 or next_pos[0] >= self.size or next_pos[1] < 0 or next_pos[1] >= self.size or self.map.get(next_pos, None) == BYTE:
                    continue
                next_length = length + 1
                if self.visited.get(next_pos, float('inf')) <= next_length:
                    continue
                self.visited[next_pos] = next_length
                heapq.heappush(stack, (next_length, next_pos))
        return self.visited.get((self.size - 1, self.size - 1), float('inf'))

    def count(self) -> Union[int, float]:
        return self.explore()


def solve1(data: str, how_many: int = 1024, size: int = 70) -> int:
    return int(Solution(data, how_many, size).count())


def solve2(data: str, size: int = 70) -> str:
    how_many_block = len(data.strip().splitlines()) - 1
    while True:
        solution = Solution(data, how_many_block, size)
        if solution.count() != float('inf'):
            return ",".join(str(n) for n in last_byte)  # noqa: F821
        last_byte: Position = solution.bytes[-1]  # noqa: F841
        how_many_block -= 1


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
