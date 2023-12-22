from typing import Union, TypeAlias, cast
from copy import deepcopy
from math import prod

Eval: TypeAlias = Union[bool, str, None]
Range: TypeAlias = list[list[int]]
RangeEval: TypeAlias = Union[Range, None]


class Rule:
    def __init__(self, raw: str):
        parts = raw.split(':')
        self.process = None
        if len(parts) == 1:
            self.process = self.eval(parts[0])
        else:
            self.cond = (({'x': 0, 'm': 1, 'a': 2, 's': 3}[parts[0][0]],
                         int.__lt__ if parts[0][1] == '<' else int.__gt__,
                         int(parts[0][2:]), parts[1]))

    def eval(self, cond: str) -> Eval:
        return True if cond == 'A' else False if cond == 'R' else cond

    def check(self, part: list[int]) -> Eval:
        if self.process is not None:
            return self.process
        return self.eval(self.cond[3]) if self.cond[1](part[self.cond[0]], self.cond[2]) else None

    def check_range(self, range_: Range) -> tuple[RangeEval, Eval, RangeEval]:
        if self.process is not None:
            return range_, self.process, None
        val_from, val_to = range_[self.cond[0]]
        if self.cond[1] == int.__lt__ and val_from >= self.cond[2] or self.cond[1] == int.__gt__ and val_to <= self.cond[2]:
            return None, None, range_
        range_1, range_2 = deepcopy(range_), deepcopy(range_)
        idx = 1 if self.cond[1] == int.__lt__ else 0
        range_1[self.cond[0]][idx] = min(range_1[self.cond[0]][1], self.cond[2] - (1 if idx else -1))
        range_2[self.cond[0]][1 - idx] = min(range_1[self.cond[0]][1] + (1 if idx else - 1), self.cond[2])
        return range_1, self.eval(self.cond[3]), None if any(from_ > to_ for from_, to_ in range_2) else range_2


class System:
    def __init__(self, raw: str):
        workflows_raw, parts_raw = raw.strip().split('\n\n')
        self.workflows = {}
        for line in workflows_raw.splitlines():
            name, rest = line.split('{')
            self.workflows[name] = [Rule(rule_raw) for rule_raw in rest[:-1].split(',')]
        self.parts = [[int(value.split('=')[1]) for value in part[1:-1].split(',')] for part in parts_raw.splitlines()]

    def check(self, part: list[int], name: str) -> bool:
        while True:
            rules = self.workflows[name]
            for rule in rules:
                result = rule.check(part)
                if isinstance(result, bool):
                    return result
                elif result is not None:
                    name = result
                    break

    def accepted(self) -> int:
        return sum(sum(part) for part in self.parts if self.check(part, 'in'))

    def check_range(self, range_left: RangeEval, label: str) -> list[Range]:
        accepted_ranges = []
        for rule in self.workflows[label]:
            range_processed, result, range_left = rule.check_range(cast(Range, range_left))
            if range_processed:
                if isinstance(result, bool):
                    if result:
                        accepted_ranges.append(range_processed)
                elif result:
                    accepted_ranges.extend(self.check_range(deepcopy(range_processed), label=result))
            if not range_left:
                break
        return accepted_ranges

    def ranges(self, max_val: int) -> int:
        return sum(prod((to_ - from_ + 1) for from_, to_ in range_) for range_ in self.check_range([[1, max_val] for n in range(4)], 'in'))


def solve1(data: str) -> int:
    return System(data).accepted()


def solve2(data: str) -> int:
    return System(data).ranges(4000)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
