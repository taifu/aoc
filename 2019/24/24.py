class Life:
    def __init__(self, raw, size=5):
        self.map = [row for row in raw.split("\n")]
        self.size = size

    def around(self, x, y):
        count = 0
        for y2 in (y - 1, y, y + 1):
            if y2 >= 0 and y2 < self.size:
                for x2 in (x - 1, x, x + 1):
                    if x2 >= 0 and x2 < self.size:
                        if y != y2 and x != x2:
                            if self.map[y2][x2] == '#':
                                count += 1
        return count

    def evolve(self):
        states = set()
        while True:
            print(self.map)
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


if __name__ == "__main__":
    life = Life(open("input.txt").read().strip())
    life.evolve()
    print(life.biodiversity)
