from math import gcd


class Map:
    def __init__(self, data: str):
        self.graph: dict[str, dict[str, str]] = {}
        lines = data.splitlines()
        self.directions: list[str] = list(lines[0])
        for line in lines[2:]:
            parts = line.replace('(', '').replace(')', '').replace(',', '').replace('=', '').split()
            self.graph[parts[0]] = {'L': parts[1], 'R': parts[2]}

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
        mcm = 1
        for count in counts:
            mcm = mcm * count // gcd(mcm, count)
        return mcm


def solve1(data: str) -> int:
    return Map(data).steps()


def solve2(data: str) -> int:
    return Map(data).steps_all()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
