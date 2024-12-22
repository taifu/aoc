from typing import TypeAlias, Dict, List, Tuple, Generator, Set, Optional, Union  # noqa: F401
from collections import defaultdict


Changes: TypeAlias = Union[Tuple[int, ...], Tuple[()]]


class Solution:
    _instance = None

    @classmethod
    def get_instance(cls, data: str) -> "Solution":
        if cls._instance is None:
            cls._instance = Solution(data)
        return cls._instance

    def __init__(self, raw: str) -> None:
        self.secrets = tuple(int(x) for x in raw.strip().splitlines())
        self.total = 0
        sequences: Dict[Changes, int] = defaultdict(int)
        for secret in self.secrets:
            last_price = secret % 10
            changes_seen = set()
            changes: Changes = ()
            for n in range(2000):
                secret = self.evolve(secret)
                price = secret % 10
                diff, last_price = price - last_price, price
                changes = changes[-3:] + (diff,)
                if n > 2 and changes not in changes_seen:
                    changes_seen.add(changes)
                    sequences[changes] += price
            self.total += secret
        self.best = max(sequences.values())

    def evolve(self, secret: int) -> int:
        secret = ((secret * 64) ^ secret) % 16777216
        secret = ((secret // 32) ^ secret) % 16777216
        secret = ((secret * 2048) ^ secret) % 16777216
        return secret

    def count(self) -> int:
        return self.total

    def count2(self) -> int:
        return self.best


def solve1(data: str) -> int:
    return Solution.get_instance(data).count()


def solve2(data: str) -> int:
    return Solution.get_instance(data).count2()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
