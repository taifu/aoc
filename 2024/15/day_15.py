from typing import TypeAlias, List, Tuple, Generator, Set, Optional  # noqa: F401


Claw: TypeAlias = Tuple[int, int, int, int, int, int]


DIRECTIONS = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
BOX_L = "["
BOX_R = "]"
EMPTY = "."
WALL = "#"


class Solution:
    def __init__(self, data: str, part2: Optional[bool] = False) -> None:
        raw1, raw2 = data.strip().split('\n\n')
        self.part2 = part2
        self.boxes = set()
        self.walls = set()
        self.map = {}
        factor = 2 if self.part2 else 1
        for y, line in enumerate(raw1.splitlines()):
            for x, char in enumerate(line):
                if self.part2:
                    if char == "#":
                        self.map[x * factor, y] = WALL
                        self.map[x * factor + 1, y] = WALL
                    elif char == "O":
                        self.map[x * factor, y] = BOX_L
                        self.map[x * factor + 1, y] = BOX_R
                    else:
                        if char == "@":
                            self.pos = (x * factor, y)
                        self.map[x * factor, y] = EMPTY
                        self.map[x * factor + 1, y] = EMPTY
                else:
                    if char == "#":
                        self.walls.add((x * factor, y))
                    elif char == "O":
                        self.boxes.add((x * factor, y))
                    elif char == "@":
                        self.pos = (x * factor, y)
        self.size = len(line)
        self.moves = [DIRECTIONS[move] for move in "".join(raw2.split('\n'))]

    def move(self, xy: Tuple[int, int], dx: int, dy: int) -> Tuple[int, int]:
        nx, ny = xy[0] + dx, xy[1] + dy
        if (nx, ny) in self.walls:
            return xy
        if (nx, ny) in self.boxes:
            nxy = self.move((nx, ny), dx, dy)
            if (nx, ny) == nxy:
                return xy
            self.boxes.remove((nx, ny))
            self.boxes.add(nxy)
        return (nx, ny)

    def draw(self) -> None:
        print()
        for y in range(self.size):
            line = ""
            for x in range(self.size * 2):
                line += self.map[x, y] if (x, y) != self.pos else "@"
            print(line)
        print()

    def count(self) -> int:
        for dx, dy in self.moves:
            self.pos = self.move(self.pos, dx, dy)
        return sum((box[1] * 100 + box[0]) for box in self.boxes)

    def count2(self) -> int:
        for dx, dy in self.moves:
            nx, ny = self.pos[0] + dx, self.pos[1] + dy
            if self.map[nx, ny] == WALL:
                continue
            if self.map[nx, ny] == EMPTY:
                self.pos = (nx, ny)
                continue
            if dy == 0:
                ex, ey = nx, ny
                while True:
                    if self.map[ex, ey] == WALL:
                        break
                    ex += dx
                    if self.map[ex, ey] == EMPTY:
                        break
                if self.map[ex, ey] == EMPTY:
                    self.pos = (nx, ny)
                    while ex != nx:
                        self.map[ex - dx, ey], self.map[ex, ey] = self.map[ex, ey], self.map[ex - dx, ey]
                        ex -= dx
            else:
                all_to_move = [[(nx, ny)]]
                if self.map[nx, ny] == BOX_L:
                    all_to_move[-1].append((nx + 1, ny))
                else:
                    all_to_move[-1].append((nx - 1, ny))
                ok = True
                cy = 0
                while True:
                    check = all_to_move[-1]
                    if any(self.map[xy[0], xy[1] + cy + dy] == WALL for xy in check):
                        ok = False
                        break
                    elif all(self.map[xy[0], xy[1] + cy + dy] == EMPTY for xy in check):
                        break
                    else:
                        next_to_move = []
                        for xy in check:
                            if self.map[xy[0], xy[1] + dy] == BOX_L:
                                move_new = ((xy[0], xy[1] + dy), (xy[0] + 1, xy[1] + dy))
                            elif self.map[xy[0], xy[1] + dy] == BOX_R:
                                move_new = ((xy[0] - 1, xy[1] + dy), (xy[0], xy[1] + dy))
                            else:
                                continue
                            if move_new not in next_to_move:
                                next_to_move.append(move_new)
                        new_to_check = []
                        for p1, p2 in next_to_move:
                            new_to_check.append(p1)
                            new_to_check.append(p2)
                        all_to_move.append(new_to_check)
                        cy = 0
                if ok:
                    self.pos = (nx, ny)
                    for to_move in all_to_move[::-1]:
                        for ex, ey in to_move:
                            self.map[ex, ey + dy], self.map[ex, ey] = self.map[ex, ey], self.map[ex, ey + dy]
        return sum((y * 100 + x) for (x, y), cell in self.map.items() if cell == BOX_L)


def solve1(data: str) -> int:
    solution = Solution(data)
    return solution.count()


def solve2(data: str) -> int:
    solution = Solution(data, True)
    return solution.count2()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
