class Row:
    def __init__(self, line: str):
        parts = line.split(' ')
        self.springs = list(parts[0] + '.')
        self.length = len(self.springs)
        self.damaged = [int(p) for p in parts[1].split(',')]
        self.cache = {}

    def arrangements(self, which=0, pos=0):
        key = (which, pos)
        try:
            return self.cache[key]
        except KeyError:
            pass
        # Last position
        if pos == self.length:
            # Ok if all block checked
            total = 1 if which == len(self.damaged) else 0
        else:
            total = 0
            # This block is ok?
            if which < len(self.damaged):
                damaged = self.damaged[which]
                if pos + damaged <= self.length and '.' not in self.springs[pos:pos + damaged] and self.springs[pos + damaged] != '#':
                    # Check next block
                    total += self.arrangements(which + 1, pos + damaged + 1)
            # Check next position for this block
            if self.springs[pos] in '.?':
                total += self.arrangements(which, pos + 1)
        self.cache[key] = total
        return total


class Field:
    def __init__(self, data: str, mult=1):
        self.rows = []
        for line in data.splitlines():
            parts = line.split(' ')
            self.rows.append(Row('?'.join([parts[0]] * mult) + ' ' + ','.join([parts[1]] * mult)))

    def arrangements(self):
        return sum(row.arrangements() for row in self.rows)


def solve1(data: str) -> int:
    return Field(data).arrangements()


def solve2(data: str) -> int:
    return Field(data, 5).arrangements()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
