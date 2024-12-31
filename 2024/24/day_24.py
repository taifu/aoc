from typing import TypeAlias, Dict, List, Tuple, Generator, Set, Optional, Union, Any, Callable  # noqa: F401
from random import randint
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
        self.zs = 0
        for line in parts[1].strip().splitlines():
            p1, op, p2, p3 = line.replace('-> ', '').split(' ')
            if p3[0] == 'z':
                self.zs += 1
            self.connections[(p1, {'AND': and_, 'XOR': xor, 'OR': or_}[op], p2)].append(p3)
        self.wires = len(self.values) // 2

    def result(self, computed: Dict[str, int]) -> int:
        result = 0
        for n in range(self.zs):
            label = 'z' + str(n).zfill(2)
            result = computed[label] * 2**n + result
        return result

    def compute(self, values: Dict[str, int]) -> Tuple[int, Optional[Order]]:
        order, computed, done = [], values.copy(), set()
        zs = 0
        while zs < self.zs:
            no_new_found = True
            for (p1, op, p2), p3s in self.connections.items():
                if (p1, op, p2) in done:
                    continue
                if p1 in computed and p2 in computed:
                    no_new_found = False
                    order.append(((p1, op, p2), p3s))
                    done.add((p1, op, p2))
                    for p3 in p3s:
                        if p3[0] == 'z':
                            zs += 1
                        computed[p3] = op(computed[p1], computed[p2])
            if no_new_found:
                return NO_CALC, None
        return self.result(computed), order

    def compute_order(self, values: Dict[str, int], order: Order) -> int:
        for (p1, op, p2), p3s in order:
            for p3 in p3s:
                values[p3] = op(values[p1], values[p2])
        return self.result(values)

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
            if n == 0:
                calc, order = self.compute(values)
            else:
                calc = self.compute_order(values, order)
            if calc == NO_CALC:
                return UNABLE
            if calc != 2**n:
                wrong.add(n)
            values[lab_x], values[lab_y] = 0, 1
            if self.compute_order(values, order) != 2**n:  # type: ignore
                wrong.add(n)
            values[lab_x] = 1
            if self.compute_order(values, order) != 2 * 2**n:  # type: ignore
                wrong.add(n)
        # Check 10 random value
        if full_check:
            for n in range(10):
                for k in values:
                    values[k] = 0
                numbers = []
                for label in ('x', 'y'):
                    x = randint(0, 2**self.wires - 1)
                    numbers.append(x)
                    for n, c in enumerate(bin(x)[2:].zfill(45)[::-1]):
                        values[label + str(n).zfill(2)] = int(c)
                if self.compute_order(values, order) != sum(numbers):  # type: ignore
                    return set([1])
        return wrong

    def count(self) -> int:
        return self.compute(self.values)[0] or 0

    def count2(self) -> str:
        # This brute force approach finds these improving swaps:
        #
        # y09 XOR x09 -> hbs <=> x09 AND y09 -> kfp  ok
        # jdm OR vvp  -> dcm <=> x22 AND y22 -> bqp
        # x17 AND y17 -> pnt <=> x18 AND y18 -> z18
        # dhq OR qdb  -> rfk <=> x18 AND y18 -> z18
        # ckj AND bch -> z27 <=> ckj XOR bch -> jcp  ok
        # ckj AND bch -> z27 <=> jcp OR knm  -> bqj
        # y21 AND x21 -> jdm <=> x22 AND y22 -> bqp
        # pvk XOR fwt -> dhq <=> x18 AND y18 -> z18  ok
        # vmg XOR rfk -> z19 <=> x18 AND y18 -> z18
        # x18 AND y18 -> z18 <=> gvb OR pnt  -> pvk
        # x18 AND y18 -> z18 <=> y18 XOR x18 -> fwt
        # x22 XOR y22 -> dbp <=> x22 AND y22 -> bqp
        # x22 AND y22 -> bqp <=> dcm XOR dbp -> pdg
        # x22 AND y22 -> bqp <=> pdg XOR tfm -> z23
        # bqp OR gkg  -> z22 <=> dcm XOR dbp -> pdg  ok
        # bqp OR gkg  -> z22 <=> pdg XOR tfm -> z23
        # dcm XOR dbp -> pdg <=> dcm AND dbp -> gkg
        #
        improving_couples = []
        start_wrong = self.wrong()
        for key1, key2 in combinations(self.connections.keys(), 2):
            self.connections[key1], self.connections[key2] = self.connections[key2], self.connections[key1]
            wrong = self.wrong()
            if wrong != UNABLE and len(wrong) < len(start_wrong):
                improving_couples.append((key1, key2))
            self.connections[key1], self.connections[key2] = self.connections[key2], self.connections[key1]
        # Try all combinations of 4 of them
        for swaps in combinations(improving_couples, 4):
            # Combinations where you swap twice same wire are not acceptable
            if len(set(key for swap in swaps for key in swap)) != 8:
                continue
            labels = []
            for key1, key2 in swaps:
                self.connections[key1], self.connections[key2] = self.connections[key2], self.connections[key1]
                labels.extend([self.connections[key1][0], self.connections[key2][0]])
            if len(self.wrong()) == 0:
                # Without a full_check there are 4 solutions without any wrong bit:
                #
                # 1) bqp,hbs,jcp,kfp,pdg,rfk,z18,z27
                #  y09 XOR x09 -> kfp <=> x09 AND y09 -> hbs
                #  dhq OR qdb  -> z18 <=> x18 AND y18 -> rfk
                #  ckj AND bch -> jcp <=> ckj XOR bch -> z27
                #  x22 AND y22 -> pdg <=> dcm XOR dbp -> bqp
                #
                # 2) hbs,jcp,kfp,pdg,rfk,z18,z22,z27
                #  y09 XOR x09 -> kfp <=> x09 AND y09 -> hbs
                #  dhq OR qdb  -> z18 <=> x18 AND y18 -> rfk
                #  ckj AND bch -> jcp <=> ckj XOR bch -> z27
                #  bqp OR gkg  -> pdg <=> dcm XOR dbp -> z22
                #
                # 3) bqp,dhq,hbs,jcp,kfp,pdg,z18,z27
                #  y09 XOR x09 -> kfp <=> x09 AND y09 -> hbs
                #  ckj AND bch -> jcp <=> ckj XOR bch -> z27
                #  pvk XOR fwt -> z18 <=> x18 AND y18 -> dhq
                #  x22 AND y22 -> pdg <=> dcm XOR dbp -> bqp
                #
                # 4) dhq,hbs,jcp,kfp,pdg,z18,z22,z27 <= only this is right: WHY!?!
                #  y09 XOR x09 -> kfp <=> x09 AND y09 -> hbs
                #  ckj AND bch -> jcp <=> ckj XOR bch -> z27
                #  pvk XOR fwt -> z18 <=> x18 AND y18 -> dhq
                #  bqp OR gkg  -> pdg <=> dcm XOR dbp -> z22
                #
                if self.wrong(True) == set():
                    return ",".join(sorted(labels))
            for key1, key2 in swaps:
                self.connections[key1], self.connections[key2] = self.connections[key2], self.connections[key1]
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
