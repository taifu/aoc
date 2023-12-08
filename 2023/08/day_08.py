from math import lcm


class Map:
    def __init__(self, data: str):
        lines = data.splitlines()
        self.graph: dict[str, dict[str, str]] = {}
        self.directions: list[str] = list(lines[0])
        for line in lines[2:]:
            self.graph[line[0:3]] = {'L': line[7:10], 'R': line[12:15]}

    def steps(self, start_from: str = 'AAA', ends: list[str] = ['ZZZ']) -> int:
        count, start = 0, start_from
        while start not in ends:
            start = self.graph[start][self.directions[count % len(self.directions)]]
            count += 1
        return count

    def steps_all(self) -> int:
        counts, starts = [], [start for start in self.graph.keys() if start[-1] == 'A']
        ends: list[str] = [end for end in self.graph.keys() if end[-1] == 'Z']
        for start in starts:
            counts.append(self.steps(start, ends))
        return lcm(*counts)


def solve1(data: str) -> int:
    return Map(data).steps()


def solve2(data: str) -> int:
    return Map(data).steps_all()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
