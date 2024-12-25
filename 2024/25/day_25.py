from typing import TypeAlias, Dict, List, Tuple, Generator, Set, Optional, Union, Any  # noqa: F401


KeyLock: TypeAlias = List[int]
Objs: TypeAlias = List[KeyLock]


class Solution:
    _instance = None

    @classmethod
    def get_instance(cls, data: str) -> "Solution":
        if cls._instance is None:
            cls._instance = Solution(data)
        return cls._instance

    def __init__(self, raw: str) -> None:
        self.keys: Objs = []
        self.locks: Objs = []
        for obj in raw.strip().split('\n\n'):
            lines = obj.strip().splitlines()
            objs = self.keys if set(lines[0]) == set('.') else self.locks
            objs.append([[lines[y][x] for y in range(len(lines))].count('#') - 1 for x in range(len(lines[0]))])

    def count(self) -> int:
        return sum(all(p < 6 for p in [x + y for x, y in zip(key, lock)]) for lock in self.locks for key in self.keys)


def solve1(data: str) -> int:
    return Solution.get_instance(data).count()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
