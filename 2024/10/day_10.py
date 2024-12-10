from typing import TypeAlias, List, Tuple, Generator, Set, Dict


Cell: TypeAlias = int
Pos: TypeAlias = Tuple[int, int]
PosCell: TypeAlias = Tuple[int, int, Cell]
Line: TypeAlias = List[int]


class Map:
    def __init__(self, data: str) -> None:
        self.map: List[Line] = []
        self.bottoms = []
        for y, line in enumerate(data.strip().split('\n')):
            self.map.append([])
            for x, char in enumerate(line):
                cell = int(char)
                self.map[-1].append(cell)
                if cell == 0:
                    self.bottoms.append((x, y))
        self.height, self.width = len(self.map), len(self.map[0])

    def around(self, x: int, y: int) -> Generator[PosCell, None, None]:
        for dx, dy in ((1, 0), (-1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                yield nx, ny, self.map[ny][nx]

    def count_peaks(self, x: int, y: int, cell: int, part2: bool = False,
                    peaks: Set[Pos] = set(), visited: Set[Pos] = set(), cache: Dict[Pos, int] = {}) -> int:
        try:
            return cache[x, y]
        except KeyError:
            visited.add((x, y))
            count = 0
            for nx, ny, next_cell in self.around(x, y):
                if part2 or (nx, ny) not in visited:
                    if next_cell == cell + 1:
                        if next_cell == 9:
                            if (nx, ny) not in peaks:
                                if not part2:
                                    peaks.add((nx, ny))
                                count += 1
                        else:
                            count += self.count_peaks(nx, ny, next_cell, part2, peaks, visited, cache)
            cache[x, y] = count
            return count

    def count(self, part2=False) -> int:
        return sum(self.count_peaks(x, y, 0, part2, set(), set(), {}) for x, y in self.bottoms)


def solve1(data: str) -> int:
    return Map(data).count()


def solve2(data: str) -> int:
    return Map(data).count(True)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
