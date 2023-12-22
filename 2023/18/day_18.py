class Plan2:
    def __init__(self, raw: str, part2: bool = False):
        self.vertical_walls = []
        self.size = [int(-10e100), int(10e100), int(-10e100), int(10e100)]
        dxy = {'3': (0, -1), '2': (-1, 0), '1': (0, 1), '0': (1, 0)}
        ys = set((0,))
        self.length = 0
        last_pos = [0, 0]
        for line in raw.splitlines():
            pos = last_pos[:]
            if part2:
                value = line.split(' ')[2][2:-1]
                length = int(value[:-1], 16)
                dxy_char = value[-1]
            else:
                parts = line.split(' ')
                length = int(parts[1])
                dxy_char = {'R': '0', 'D': '1', 'L': '2', 'U': '3'}[parts[0][0]]
            backward = dxy_char in '23'
            vertical = dxy_char in '31'
            self.length += length
            for n in range(2):
                pos[n] += dxy[dxy_char][n] * length
            wall = (pos + last_pos) if backward else (last_pos + pos)
            ys.add(pos[1])
            if vertical:
                self.vertical_walls.append(wall)
            for n, xy in enumerate(pos):
                for m, fun in enumerate((max, min)):
                    self.size[n * 2 + m] = fun(self.size[n * 2 + m], xy)
            last_pos = pos
        self.ys = sorted(ys)

    def vertical_intercepts(self, y0: int, y1: int) -> list[int]:
        return sorted(set([x for wall in self.vertical_walls
                           if wall[1] < y1 and wall[3] > y0 for x in (wall[0], wall[2])]))

    def area(self) -> int:
        area = 0
        for y0_slice, y1_slice in zip(self.ys, self.ys[1:]):
            x_slices = self.vertical_intercepts(y0_slice, y1_slice)
            pair = 0
            if self.size[0] not in x_slices:
                pair = 1
                x_slices.insert(0, self.size[0])
            if self.size[2] not in x_slices:
                x_slices.append(self.size[2])
            for x0, x1 in zip(x_slices[pair::2], x_slices[pair + 1::2]):
                area += (y1_slice - y0_slice) * (x1 - x0)
        return area + self.length // 2 + 1


def solve1(data: str) -> int:
    return Plan2(data).area()


def solve2(data: str) -> int:
    return Plan2(data, True).area()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
