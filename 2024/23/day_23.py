from typing import TypeAlias, Dict, List, Tuple, Generator, Set, Optional, Union  # noqa: F401
from collections import defaultdict
from itertools import combinations


Changes: TypeAlias = Union[Tuple[int, ...], Tuple[()]]


class Solution:
    _instance = None

    @classmethod
    def get_instance(cls, data: str) -> "Solution":
        if cls._instance is None:
            cls._instance = Solution(data)
        return cls._instance

    def __init__(self, raw: str) -> None:
        self.connections = defaultdict(set)
        for line in raw.strip().splitlines():
            pc1, pc2 = line.split('-')
            self.connections[pc1].add(pc2)
            self.connections[pc2].add(pc1)
        self.chief = set()
        max_lan_party: Tuple[int, Set[str]] = (0, set())
        for pc0, pcs in self.connections.items():
            # Part 1
            if pc0[0] == 't':
                for pc1, pc2 in combinations(pcs, 2):
                    if (pc0 in self.connections[pc1] and pc2 in self.connections[pc1] and  # noqa: W504
                            pc1 in self.connections[pc2] and pc0 in self.connections[pc2]):
                        self.chief.add(frozenset((pc0, pc1, pc2)))
            # Part 2
            lan_party = set([pc0])
            for pc1 in pcs:
                if all(pc1 in self.connections[pc2] for pc2 in lan_party):
                    lan_party.add(pc1)
            if len(lan_party) > max_lan_party[0]:
                max_lan_party = (len(lan_party), lan_party)
        self.largest_lan_party = max_lan_party[1]

    def count(self) -> int:
        return len(self.chief)

    def count2(self) -> str:
        return ','.join(sorted(self.largest_lan_party))


def solve1(data: str) -> int:
    return Solution.get_instance(data).count()


def solve2(data: str) -> str:
    return Solution.get_instance(data).count2()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
