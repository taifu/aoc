from collections import defaultdict
from math import sqrt, prod


class Playground:
    def __init__(self, data: str) -> None:
        self.junctions = []
        self.junctions_circuits = {}
        self.distances = []
        self.circuits = defaultdict(set)
        for line in data.strip().splitlines():
            self.junctions.append(tuple(int(c) for c in line.split(',')))
            for junction in self.junctions[:-1]:
                d = self.distance(junction, self.junctions[-1])
                self.distances.append((d, junction, self.junctions[-1]))

    def distance(self, j1, j2) -> int:
        return sqrt(sum((j1[d] - j2[d])**2 for d in range(3)))

    def connect(self, connections: int) -> None:
        conn = 0
        for key, j1, j2 in sorted(self.distances):
            conn += 1
            circ1, circ2 = self.junctions_circuits.get(j1), self.junctions_circuits.get(j2)
            if circ1 is None or circ2 is None:
                if circ1 is None and circ2 is None:
                    circuit = conn
                    self.circuits[circuit].add(j1)
                    self.circuits[circuit].add(j2)
                    self.junctions_circuits[j1] = conn
                    self.junctions_circuits[j2] = conn
                elif circ1 is None:
                    self.junctions_circuits[j1] = circ2
                    self.circuits[circ2].add(j1)
                else:
                    self.junctions_circuits[j2] = circ1
                    self.circuits[circ1].add(j2)
            elif circ1 != circ2:
                for junction in self.circuits[circ2]:
                    self.junctions_circuits[junction] = circ1
                    self.circuits[circ1].add(junction)
                del self.circuits[circ2]
            if conn == connections:
                self.part1 = prod(sorted(list(len(juncts) for juncts in self.circuits.values()))[-3:])
            if len(self.circuits) == 1 and len(list(self.circuits.values())[0]) == len(self.junctions):
                self.part2 = j1[0] * j2[0]
                break
        return self


playground = None


def load(data: str) -> Playground:
    global playground
    if playground is None:
        playground = Playground(data)
    return playground


def solve1(data: str, connections: int = 1000) -> int:
    play = load(data)
    return play.connect(connections).part1


def solve2(data: str) -> int:
    play = load(data)
    return play.part2


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
