from typing import TypeAlias, Dict, List, Tuple, Generator, Set, Optional, Union, Any, Callable  # noqa: F401
from operator import and_, or_, xor
from collections import defaultdict
from itertools import combinations


Changes: TypeAlias = Union[Tuple[int, ...], Tuple[()]]
Order: TypeAlias = List[Tuple[Tuple[str, Callable[[int, int], int], str], List[str]]]


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

    def result(self, computed: Dict[str, int]) -> int:
        result, n = '', 0
        while True:
            label = 'z' + str(n).zfill(2)
            if label not in computed:
                break
            result = str(computed[label]) + result
            n += 1
        return int(result, 2)

    def compute(self, values: Dict[str, int]) -> Tuple[int, Optional[Order]]:
        order = []
        computed = values.copy()
        done = set()
        while len(computed) - len(values) < len(self.connections):
            found = False
            for (p1, op, p2), p3s in self.connections.items():
                if (p1, op, p2) in done:
                    continue
                if p1 in computed and p2 in computed:
                    found = True
                    order.append(((p1, op, p2), p3s))
                    done.add((p1, op, p2))
                    for p3 in p3s:
                        computed[p3] = op(computed[p1], computed[p2])
            if not found:
                return NO_CALC, None
        result = self.result(computed)
        return result, order

    def compute_order(self, values: Dict[str, int], order: Order) -> int:
        computed = values.copy()
        for (p1, op, p2), p3s in order:
            for p3 in p3s:
                computed[p3] = op(computed[p1], computed[p2])
        return self.result(computed)

    def wrong(self, full_check: Optional[bool] = False) -> Set[int]:
        wrong = set()
        order = None
        values = self.values.copy()
        for n in range(self.wires):
            for k in values:
                values[k] = 0
            lab_x = f"x{str(n).zfill(2)}"
            lab_y = f"y{str(n).zfill(2)}"
            values[lab_x] = 1
            if order is None:
                calc, order = self.compute(values)
            else:
                calc = self.compute_order(values, order)
            if calc == NO_CALC:
                return UNABLE
            if calc != 2 ** n:
                wrong.add(n)
            values[lab_x], values[lab_y] = 0, 1
            if self.compute_order(values, order) != 2 ** n:  # type: ignore
                wrong.add(n)
            values[lab_x] = 1
            if self.compute_order(values, order) != 2 * 2 ** n:  # type: ignore
                wrong.add(n)
        # Check 100 random value
        if full_check:
            from random import randint
            values = self.values.copy()
            for n in range(100):
                for k in values:
                    values[k] = 0
                numbers = []
                for label in ('x', 'y'):
                    x = randint(0, 2**45 - 1)
                    numbers.append(x)
                    for n, c in enumerate(bin(x)[2:].zfill(45)[::-1]):
                        values[label + str(n).zfill(2)] = int(c)
                if self.compute_order(values, order) != sum(numbers):  # type: ignore
                    return set([1])
        return wrong

    def count(self) -> int:
        return self.compute(self.values)[0] or 0

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
