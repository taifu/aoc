from typing import TypeAlias, Dict, List, Tuple, Generator, Set, Optional, Union, Any  # noqa: F401
from operator import and_, or_, xor
from collections import defaultdict
from itertools import combinations


Changes: TypeAlias = Union[Tuple[int, ...], Tuple[()]]


NO_CALC = -1
UNABLE = set((-1,))


class Solution:
    _instance = None

    @classmethod
    def get_instance(cls, data: str) -> "Solution":
        if cls._instance is None:
            cls._instance = Solution(data)
        return cls._instance

    def __init__(self, raw: str) -> None:
        parts = raw.strip().split('\n\n')
        self.values = {}
        for line in parts[0].strip().splitlines():
            p1, p2 = line.split(':')
            self.values[p1] = int(p2.strip())
        self.connections = defaultdict(list)
        for line in parts[1].strip().splitlines():
            p1, op, p2, p3 = line.replace('-> ', '').split(' ')
            self.connections[(p1, {'AND': and_, 'XOR': xor, 'OR': or_}[op], p2)].append(p3)
        self.wires = len(self.values) // 2

    def compute(self, values: Dict[str, int]) -> int:
        values = values.copy()
        connections = self.connections.copy()
        last_conn, last_val = (len(connections), len(values))
        while connections:
            for (p1, op, p2), p3s in connections.copy().items():
                if not (p1 in values or p2 in values) and not (isinstance(p1, int) and isinstance(p2, int)):
                    continue
                connections.pop((p1, op, p2))
                both = True
                if not isinstance(p1, int):
                    if p1 in values:
                        p1 = values[p1]  # type: ignore
                    else:
                        both = False
                if not isinstance(p2, int):
                    if p2 in values:
                        p2 = values[p2]  # type: ignore
                    else:
                        both = False
                if both:
                    for p3 in p3s:
                        values[p3] = op(p1, p2)
                else:
                    connections[(p1, op, p2)] = p3s
            if (last_conn, last_val) == (len(connections), len(values)):
                return NO_CALC
            last_conn, last_val = (len(connections), len(values))
        result, n = '', 0
        while True:
            label = 'z' + str(n).zfill(2)
            if label not in values:
                break
            result = str(values[label]) + result
            n += 1
        return int(result, 2)

    def wrong(self, full_check: Optional[bool] = False) -> Set[int]:
        wrong = set()
        for n in range(self.wires):
            values = self.values.copy()
            for k in values:
                values[k] = 0
            lab_x = f"x{str(n).zfill(2)}"
            lab_y = f"y{str(n).zfill(2)}"
            values[lab_x] = 1
            # calc = self.compute(values)
            calc = self.compute(values)
            if calc == NO_CALC:
                return UNABLE
            if calc != 2 ** n:
                wrong.add(n)
            values[lab_x] = 0
            values[lab_y] = 1
            # calc = self.compute(values)
            calc = self.compute(values)
            if calc != 2 ** n:
                wrong.add(n)
            values[lab_x] = 1
            # calc = self.compute(values)
            calc = self.compute(values)
            if calc != 2 * 2 ** n:
                wrong.add(n)
        # Testare valori a caso
        if full_check:
            from random import randint
            for n in range(100):
                values = self.values.copy()
                for k in values:
                    values[k] = 0
                numbers = []
                for label in ('x', 'y'):
                    x = randint(0, 2**45 - 1)
                    numbers.append(x)
                    for n, c in enumerate(bin(x)[2:].zfill(45)[::-1]):
                        values[label + str(n).zfill(2)] = int(c)
                calc = self.compute(values)
                if (calc != sum(numbers)):
                    return set([1])
        return wrong

    def count(self) -> int:
        return self.compute(self.values) or 0

    def count2(self) -> str:
        keys = list(self.connections.keys())
        n_conn = len(keys)
        improving = []
        start_wrong = self.wrong()
        # This brute force approach finds these improving swaps:
        # (30, 94)
        # (34, 157)
        # (57, 136)
        # (81, 136)
        # (87, 109)
        # (87, 177)
        # (104, 157)
        # (108, 136)
        # (134, 136)
        # (136, 164)
        # (136, 174)
        # (145, 157)
        # (157, 173)
        # (157, 206)
        # (168, 173)
        # (168, 206)
        # (173, 184)
        for sw1, sw2 in combinations(range(n_conn), 2):
            self.connections[keys[sw1]], self.connections[keys[sw2]] = self.connections[keys[sw2]], self.connections[keys[sw1]]
            wrong = self.wrong()
            if wrong != UNABLE and len(wrong) < len(start_wrong):
                improving.append((sw1, sw2))
            self.connections[keys[sw1]], self.connections[keys[sw2]] = self.connections[keys[sw2]], self.connections[keys[sw1]]
        # Try all combinations of 4 of them
        for swaps in combinations(improving, 4):
            if len(set(wire for swap in swaps for wire in swap)) < 8:
                continue
            labels = []
            for sw1, sw2 in swaps:
                self.connections[keys[sw1]], self.connections[keys[sw2]] = self.connections[keys[sw2]], self.connections[keys[sw1]]
                labels.append(self.connections[keys[sw1]][0])
                labels.append(self.connections[keys[sw2]][0])
            wrong = self.wrong()
            if wrong != UNABLE and len(wrong) == 0:
                # Without a full_check there are 4 solutions
                # ((30, 94), (81, 136), (87, 109), (157, 173))
                # bqp,hbs,jcp,kfp,pdg,rfk,z18,z27
                # ((30, 94), (81, 136), (87, 109), (168, 173))
                # hbs,jcp,kfp,pdg,rfk,z18,z22,z27
                # ((30, 94), (87, 109), (108, 136), (157, 173))
                # bqp,dhq,hbs,jcp,kfp,pdg,z18,z27
                # ((30, 94), (87, 109), (108, 136), (168, 173))
                # dhq,hbs,jcp,kfp,pdg,z18,z22,z27            <- only this was right: WHY!?!
                if self.wrong(True) == set():
                    return ",".join(sorted(labels))
            for sw1, sw2 in swaps:
                self.connections[keys[sw1]], self.connections[keys[sw2]] = self.connections[keys[sw2]], self.connections[keys[sw1]]
        return ""


def solve1(data: str) -> int:
    return Solution.get_instance(data).count()


def solve2(data: str) -> str:
    return Solution.get_instance(data).count2()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
