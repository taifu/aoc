class Universe:
    def __init__(self, data: str):
        self.space: list[list[str]] = list(list(line) for line in data.splitlines())
        self.height, self.width = len(self.space), len(self.space[0])
        self.empty_rows: list[int] = sorted([n for n, row in enumerate(self.space) if len(set(row)) == 1])
        self.empty_columns: list[int] = sorted([n for n in range(self.width) if len(set([self.space[m][n]
                                                for m in range(self.height)])) == 1])
        self.galaxies: list[tuple[int, int]] = [(x, y) for y in range(self.width)
                                                for x, space in enumerate(self.space[y]) if space == '#']

    def how_many(self, empties: list[int], pos1: int, pos2: int) -> int:
        if pos1 > pos2:
            pos2, pos1 = pos1, pos2
        if pos2 - pos1 < 2:
            return 0
        count = 0
        for n in range(pos1 + 1, pos2):
            if n in empties:
                count += 1
        return count

    def shortest(self, emptyness: int = 2) -> int:
        shortest = 0
        for n, galaxy1 in enumerate(self.galaxies):
            for galaxy2 in self.galaxies[n + 1:]:
                distance = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])
                distance += self.how_many(self.empty_rows, galaxy1[1], galaxy2[1]) * (emptyness - 1)
                distance += self.how_many(self.empty_columns, galaxy1[0], galaxy2[0]) * (emptyness - 1)
                shortest += distance
        return shortest


def solve1(data: str) -> int:
    return Universe(data).shortest()


def solve2(data: str, emptyness: int = 1000000) -> int:
    return Universe(data).shortest(emptyness)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
