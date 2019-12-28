from functools import lru_cache


class Life:
    def __init__(self, raw, size=5):
        self.map = [row for row in raw.split("\n")]
        self.size = size

    def around(self, x, y):
        count = 0
        for x2, y2 in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
            if y2 >= 0 and y2 < self.size:
                if x2 >= 0 and x2 < self.size:
                    if self.map[y2][x2] == '#':
                        count += 1
        return count

    def evolve(self):
        states = set()
        while True:
            if self.state in states:
                return
            states.add(self.state)
            new_map = []
            for y, row in enumerate(self.map):
                new_row = ""
                for x in range(len(row)):
                    count = self.around(x, y)
                    if row[x] == '#' and count != 1:
                        new_row += '.'
                    elif row[x] == '.' and count in (1, 2):
                        new_row += '#'
                    else:
                        new_row += row[x]
                new_map.append(new_row)
            self.map = new_map

    @property
    def state(self):
        return "".join(row for row in self.map)

    @property
    def biodiversity(self):
        bio = 0
        current = 1
        for row in self.map:
            for c in row:
                if c == '#':
                    bio += current
                current *= 2
        return bio


class LifeRec:
    def __init__(self, raw, size=5):
        self.size = size
        data = raw.split("\n")
        self.bugs = set((x, y, 0) for x in range(5) for y in range(5) if data[y][x] == "#")
    
    @lru_cache(maxsize=None)
    def around(self, x, y, depth):
        cells = []
        for x2, y2 in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
            if y2 >= 0 and y2 < self.size:
                if x2 >= 0 and x2 < self.size:
                    if x2 != 2 or y2 != 2:
                        cells.append((x2, y2, depth))
                    else:
                        if x == 2:
                            for x3 in range(5):
                                cells.append((x3, 0 if y == 1 else self.size - 1, depth + 1))
                        else:
                            assert y == 2
                            for y3 in range(5):
                                cells.append((0 if x == 1 else self.size - 1, y3, depth + 1))
                else:
                    cells.append((1 if x2 < 0 else 3, 2, depth - 1))
            else:
                cells.append((2, 1 if y2 < 0 else 3, depth - 1))
        return cells

    def evolve(self, steps):
        for step in range(steps):
            bugs = set()
            seen = set()
            for bug in self.bugs:
                seen.add(bug)
                count = sum(1 for cell in self.around(*bug) if cell in self.bugs)
                if count == 1:
                    bugs.add(bug)
                for cell in self.around(*bug):
                    if cell not in seen and cell not in self.bugs:
                        seen.add(cell)
                        count = sum(1 for cell2 in self.around(*cell) if cell2 in self.bugs)
                        if count in (1, 2):
                            bugs.add(cell)
            self.bugs = bugs


if __name__ == "__main__":
    raw = open("input.txt").read().strip()
    life = Life(raw)
    life.evolve()
    print(life.biodiversity)
    life = LifeRec(raw)
    life.evolve(200)
    print(len(life.bugs))
