from collections import defaultdict


def load(data):
    elves = set()
    for y, line in enumerate(data.split('\n')):
        for x, char in enumerate(line):
            if char == '#':
                elves.add(x + 1j * y)
    return elves


class Elves:
    def __init__(self, elves):
        self.elves = load(elves)

    def draw(self):
        print()
        for y in self.range_y:
            line = f"{y:03} "
            for x in self.range_x:
                line += "." if (x + 1j * y) not in self.elves else "#"
            print(line)
        print()

    @property
    def range_x(self):
        return range(int(min(elf.real for elf in self.elves)), int(max(elf.real for elf in self.elves)) + 1)

    @property
    def range_y(self):
        return range(int(min(elf.imag for elf in self.elves)), int(max(elf.imag for elf in self.elves)) + 1)


    def move(self, rounds=None):
        searches = [(-1j, -1 - 1j, 1 - 1j), (1j, -1 + 1j, 1 + 1j), (-1, -1 + 1j, -1 - 1j), (1, 1 + 1j, 1 - 1j)]
        round_ = -1
        while True:
            if (round_ := round_ + 1) == rounds:
                break
            next_elves, moving_elves = set(), defaultdict(list)
            for elf in self.elves:
                if any((elf + pos_around) in self.elves for pos_around in (-1 - 1j, -1j, 1 - 1j, -1, 1, -1 + 1j, +1j, 1 + 1j)):
                    for good_search in range(round_ % 4, round_ % 4 + 4):
                        if not any((elf + pos_around) in self.elves for pos_around in searches[good_search % 4]):
                            moving_elves[elf + searches[good_search % 4][0]].append(elf)
                            break
                    else:
                        next_elves.add(elf)
                else:
                    next_elves.add(elf)
            for moving_elf, how_many in moving_elves.items():
                if len(how_many) > 1:
                    for elf in how_many:
                        next_elves.add(elf)
                else:
                    next_elves.add(moving_elf)
            if len(moving_elves) == 0 and rounds is None:
                # Part 2
                return round_ + 1
            self.elves = next_elves
        # Part 1
        return int(len(self.range_x) * len(self.range_y) - len(self.elves))


def solve1(data):
    return Elves(data).move(10)


def solve2(data):
    return Elves(data).move()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
