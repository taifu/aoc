class Digits:
    def __init__(self, line):
        self.wirings, self.output = tuple(list(frozenset(p) for p in part.strip().split(" ")) for part in line.split("|"))

    def easy(self):
        return sum(1 for wiring in self.output if len(wiring) in (2, 3, 4, 7))

    def discover(self, wirings, length, subtract=set()):
        found = [wiring for wiring in wirings if len(wiring - subtract) == length][0]
        wirings.remove(found)
        return found, wirings

    def value(self, digit_segments):
        return sum(digit_segments[wiring] * 10**p for p, wiring in enumerate(reversed(self.output)))

    def decode(self):
        digits = {}
        digits[8], left_012345679 = self.discover(self.wirings, 7)
        digits[1], left_02345679 = self.discover(left_012345679, 2)
        digits[4], left_0235679 = self.discover(left_02345679, 4)
        digits[7], left_023569 = self.discover(left_0235679, 3)
        segment_a = digits[7] - digits[1]
        digits[3], left_02569 = self.discover(left_023569, 3, digits[1])
        digits[6], left_0259 = self.discover(left_02569, 5, digits[1])
        digits[0], left_259 = self.discover(left_0259, 2, digits[3])
        digits[9], left_25 = self.discover(left_259, 5, segment_a)
        digits[2], left_5 = self.discover(left_25, 3, digits[4])
        digits[5] = left_5[0]
        return self.value({frozenset(v): k for k, v in digits.items()})


def load(data):
    return [Digits(line) for line in data.strip().split("\n")]


def solve1(data):
    return sum(digit.easy() for digit in load(data))


def solve2(data):
    return sum(digit.decode() for digit in load(data))


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
