from typing import TypeAlias, Dict, List, Tuple, Generator, Set, Optional, Union, Any, Type  # noqa: F401
from enum import Enum
from itertools import pairwise
from functools import cache


class Numpad(Enum):
    KA = 'A'
    K0 = '0'
    K1 = '1'
    K2 = '2'
    K3 = '3'
    K4 = '4'
    K5 = '5'
    K6 = '6'
    K7 = '7'
    K8 = '8'
    K9 = '9'
    GP = ' '


class Dirpad(Enum):
    KA = 'A'
    KU = '^'
    KD = 'v'
    KL = '<'
    KR = '>'
    GP = ' '


Key: TypeAlias = Union[str, Dirpad, Numpad, Enum]
Position: TypeAlias = Tuple[int, int]
KeyPath: TypeAlias = Union[Tuple[Key, ...], Tuple[()]]
KeyPaths: TypeAlias = Union[Tuple[KeyPath, ...], Tuple[()]]

POS: Dict[Key, Position] = {
    Numpad.K7: (0, 0),
    Numpad.K8: (1, 0),
    Numpad.K9: (2, 0),
    Numpad.K4: (0, 1),
    Numpad.K5: (1, 1),
    Numpad.K6: (2, 1),
    Numpad.K1: (0, 2),
    Numpad.K2: (1, 2),
    Numpad.K3: (2, 2),
    Numpad.GP: (0, 3),
    Numpad.K0: (1, 3),
    Numpad.KA: (2, 3),
    Dirpad.GP: (0, 0),
    Dirpad.KU: (1, 0),
    Dirpad.KA: (2, 0),
    Dirpad.KL: (0, 1),
    Dirpad.KD: (1, 1),
    Dirpad.KR: (2, 1),
}
DXY_KEYS = {
    (0, -1): Dirpad.KU,
    (0, 1): Dirpad.KD,
    (1, 0): Dirpad.KR,
    (-1, 0): Dirpad.KL,
}
POS_NUMPAD: Dict[Position, Key] = dict((POS[k], k) for k in Numpad)
POS_DIRPAD: Dict[Position, Key] = dict((POS[k], k) for k in Dirpad)


class Solution:
    _instance = None

    @classmethod
    def get_instance(cls, data: str) -> "Solution":
        if cls._instance is None:
            cls._instance = Solution(data)
        return cls._instance

    def __init__(self, raw: str) -> None:
        self.sequences = []
        for line in raw.strip().splitlines():
            self.sequences.append((tuple(Numpad(key) for key in tuple(line)), int(line[:3])))
        self.all_paths_numpad = self.all_paths(Numpad, POS_NUMPAD)
        self.all_paths_dirpad = self.all_paths(Dirpad, POS_DIRPAD)

    def shortest_paths(self, key_from: Key, key_to: Key, pos_keys: Dict[Position, Key], forbidden: Position) -> KeyPaths:
        if key_from == key_to:
            return ((Dirpad.KA,),)
        paths: KeyPaths = ()
        x1, y1 = POS[key_from]
        x2, y2 = POS[key_to]
        dx = 1 if x2 > x1 else (-1 if x2 < x1 else 0)
        dy = 1 if y2 > y1 else (-1 if y2 < y1 else 0)
        # Move right/left
        if dx:
            if (x1 + dx, y1) != forbidden:
                key_dir = DXY_KEYS[dx, 0]
                for path in self.shortest_paths(pos_keys[x1 + dx, y1], key_to, pos_keys, forbidden):
                    paths += (((key_dir,) + path),)
        # Move up/down
        if dy:
            if (x1, y1 + dy) != forbidden:
                key_dir = DXY_KEYS[0, dy]
                for path in self.shortest_paths(pos_keys[x1, y1 + dy], key_to, pos_keys, forbidden):
                    paths += (((key_dir,) + path),)
        return tuple(paths)

    def all_paths(self, keypad: Type[Dirpad] | Type[Numpad], pos_keys: Dict[Position, Key]) -> Dict[Tuple[Key, Key], Tuple[KeyPath, ...]]:
        all_paths: Dict[Tuple[Key, Key], KeyPaths] = {}
        for k_from in keypad:
            if k_from == keypad.GP:
                continue
            for k_to in keypad:
                if k_to == keypad.GP:
                    continue
                if k_from == k_to:
                    all_paths[k_from, k_to] = ((keypad['KA'],),)
                else:
                    all_paths[k_from, k_to] = self.shortest_paths(k_from, k_to, pos_keys, POS[keypad.GP])
        return all_paths

    @cache
    def press(self, key_from: Key, key_to: Key, levels: int) -> int:
        if levels == 1:
            return len(self.all_paths_dirpad[key_from, key_to][0])
        all_lengths = []
        for path in self.all_paths_dirpad[key_from, key_to]:
            all_lengths.append(sum(self.press(key_0, key_1, levels - 1) for key_0, key_1 in pairwise((Dirpad.KA,) + path)))
        return min(all_lengths)

    def count(self, levels: int = 3) -> int:
        complexity = 0
        for sequence, code in self.sequences:
            all_paths: KeyPaths = ()
            last_key = Numpad.KA
            for next_key in sequence:
                this_paths: KeyPaths = ()
                for path in self.all_paths_numpad[last_key, next_key]:
                    this_paths += (path,)
                all_paths = tuple([aseq + dseq for dseq in this_paths for aseq in all_paths] or this_paths)
                last_key = next_key
            lengths = []
            for path in all_paths:
                lengths.append(sum(self.press(k0, k1, levels) for k0, k1 in pairwise((Dirpad.KA,) + path)))
            complexity += code * min(lengths)
        return complexity


def solve1(data: str, levels: int = 2) -> int:
    return Solution.get_instance(data).count(levels)


def solve2(data: str) -> int:
    return Solution.get_instance(data).count(levels=25)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
