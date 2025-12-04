type Pos = complex
type Map = set[Pos]
type Around = tuple[Pos, ...]

PAPER = '@'


class Department:
    def __init__(self, data: str) -> None:
        self.height: int = 0
        self.map: Map = set()
        for self.width, line in enumerate(data.strip().splitlines()):
            self.map.update(complex(x, self.width) for x, char in enumerate(line) if char == PAPER)
            self.height += 1
        self.width += 1

    def pos_around(self, pos: Pos) -> Around:
        return tuple(pos + dxy for dxy in (1, -1, 1j, -1j, 1 + 1j, 1 - 1j, -1 - 1j, -1 + 1j)
                     if 0 <= (pos + dxy).real < self.width and 0 <= (pos + dxy).imag < self.height)

    def is_accessible(self, pos: Pos) -> bool:
        return sum(1 if around in self.map else 0 for around in self.pos_around(pos)) < 4

    def accessibles(self) -> int:
        return sum(1 for pos in self.map if self.is_accessible(pos))

    def removables(self) -> int:
        tot = 0
        while True:
            if not (to_remove := tuple(pos for pos in self.map if self.is_accessible(pos))):
                break
            tot += len(to_remove)
            self.map -= set(to_remove)
        return tot


def load(data: str) -> Department:
    return Department(data)


def solve1(data: str) -> int:
    return load(data).accessibles()


def solve2(data: str) -> int:
    return load(data).removables()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
