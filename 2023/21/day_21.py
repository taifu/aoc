from typing import TypeAlias, Generator, Union
from collections import deque

Around: TypeAlias = Generator[tuple[int, int], None, None]
Cell: TypeAlias = Union[tuple[int, int], None]


class Map:
    def __init__(self, raw: str):
        self.map = []
        for line in raw.splitlines():
            self.map.append(['.' if char == 'S' else char for char in line])
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.start = (self.width // 2, self.height // 2)

    def around(self, x: int, y: int) -> Around:
        for d_y in (-1, 0, 1):
            if 0 <= y + d_y < self.height:
                for d_x in (-1, 0, 1):
                    if abs(d_y) + abs(d_x) != 1:
                        continue
                    if 0 <= x + d_x < self.width:
                        if self.map[y + d_y][x + d_x] == '.':
                            yield (x + d_x, y + d_y)

    def draw(self, seen: set[tuple[int, int]]) -> None:
        print()
        for y in range(self.height):
            print(''. join('S' if (x, y) == self.start and len(seen) == 0 else 'O'
                           if (x, y) in seen else str(self.map[y][x]) for x in range(self.width)))
        print()

    def reach(self, max_steps: int = 0, start: Cell = None) -> list[int]:
        if not start:
            start = self.start
        cells = deque(((start, 0),))
        seen = set()
        evens_odds = [0, 0]
        while cells:
            cell, steps = cells.popleft()
            evens_odds[steps % 2] += 1
            seen.add(cell)
            if max_steps == 0 or steps < max_steps:
                for next_cell in self.around(*cell):
                    if next_cell in seen:
                        continue
                    seen.add(next_cell)
                    cells.append((next_cell, steps + 1))
        return evens_odds

    def inf_reach(self, max_steps: int) -> int:
        assert self.width == self.height
        size = self.width
        #
        # ----------------|---------------|--------------|---------------|----------------
        #      empty      |nw_almost_empty| n_almost_full|ne_almost_empty|     empty
        # ----------------|---------------|--------------|---------------|----------------
        #  nw_almost_empty nw_almost_full |   odd_full   |ne_almost_full | ne_almost_empty
        # ----------------|---------------|--------------|---------------|----------------
        #  w_almost_full  |    odd_full   |  even_full   |  odd_full     | e_almost_full
        # ----------------|---------------|--------------|---------------|----------------
        #  sw_almost_empty|sw_almost_full |   odd_full   |se_almost_full | se_almost_empty
        # ----------------|---------------|--------------|---------------|----------------
        #      empty      |sw_almost_empty| s_almost_full|se_almost_empty|     empty
        # ----------------|---------------|--------------|---------------|----------------
        #
        parity = max_steps % 2

        even_full, odd_full = self.reach()
        if parity:
            odd_full, even_full = even_full, odd_full

        steps_left_from_middle = (max_steps - 1 - size // 2) % size
        steps_left_from_full_corner = size // 2 + steps_left_from_middle
        steps_left_from_empty_corner = steps_left_from_middle - size // 2

        nw_almost_empty = self.reach(steps_left_from_empty_corner, (size - 1, size - 1))[1 - parity]
        ne_almost_empty = self.reach(steps_left_from_empty_corner, (0, size - 1))[1 - parity]
        sw_almost_empty = self.reach(steps_left_from_empty_corner, (size - 1, 0))[1 - parity]
        se_almost_empty = self.reach(steps_left_from_empty_corner, (0, 0))[1 - parity]

        nw_almost_full = self.reach(steps_left_from_full_corner, (size - 1, size - 1))[parity]
        ne_almost_full = self.reach(steps_left_from_full_corner, (0, size - 1))[parity]
        sw_almost_full = self.reach(steps_left_from_full_corner, (size - 1, 0))[parity]
        se_almost_full = self.reach(steps_left_from_full_corner, (0, 0))[parity]

        n_almost_full = self.reach(steps_left_from_middle, (size // 2, 0))[1 - parity]
        e_almost_full = self.reach(steps_left_from_middle, (0, size // 2))[1 - parity]
        w_almost_full = self.reach(steps_left_from_middle, (size - 1, size // 2))[1 - parity]
        s_almost_full = self.reach(steps_left_from_middle, (size // 2, size - 1))[1 - parity]

        repeat = max_steps // size

        # Cardinal points grids
        total = n_almost_full + w_almost_full + e_almost_full + s_almost_full

        # Full inside grids
        total += odd_full * repeat**2
        total += even_full * (repeat - 1)**2

        # Diagonal almost empty grids
        total += (nw_almost_empty + ne_almost_empty + se_almost_empty + sw_almost_empty) * repeat

        # Diagonal almost full grids
        total += (nw_almost_full + ne_almost_full + se_almost_full + sw_almost_full) * (repeat - 1)

        return total


def solve1(data: str, steps: int = 64) -> int:
    return Map(data).reach(steps)[0]


def solve2(data: str, steps: int = 26501365) -> int:
    return Map(data).inf_reach(steps)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
