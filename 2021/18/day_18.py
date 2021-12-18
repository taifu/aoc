import itertools


def add(snailfish, number, at_pos):
    left, right = snailfish[:at_pos], snailfish[at_pos:]
    original = ""
    while left and left[-1].isdigit():
        original, left = left[-1] + original, left[:-1]
    while right and right[0].isdigit():
        original, right = original + right[0], right[1:]
    return left + str(number + int(original)) + right


def find_digit(snailfish, left=True):
    start, mult = (1, -1) if left else (0, 1)
    pos_digit = None
    for pos in range(start, len(snailfish)):
        if snailfish[pos * mult].isdigit():
            pos_digit = pos
        elif pos_digit is not None:
            break
    return pos_digit


def explode(snailfish):
    opened = 0
    for pos_opened, c in enumerate(snailfish):
        if c == '[':
            opened += 1
        elif c == ']':
            opened -= 1
        if opened == 5:
            pos_opened += 1
            pos_closed = snailfish[pos_opened:].index("]")
            left, pair, right = (snailfish[:pos_opened],
                                 snailfish[pos_opened:pos_opened + pos_closed],
                                 snailfish[pos_opened + pos_closed:])
            n1, n2 = (int(p) for p in pair.split(','))
            pos_add = find_digit(left, True)
            if pos_add is not None:
                left = add(left, n1, len(left) - pos_add)
            pos_add = find_digit(right, False)
            if pos_add is not None:
                right = add(right, n2, pos_add)
            return left[:-1] + "0" + right[1:], True
    return snailfish, False


def split(snailfish):
    for pos_digit, c in enumerate(snailfish):
        if c.isdigit():
            end_digit = pos_digit
            while snailfish[end_digit].isdigit():
                end_digit += 1
            value = int(snailfish[pos_digit:end_digit])
            if value > 9:
                return snailfish[:pos_digit] + f"[{value//2},{(value + 1)//2}]" + snailfish[end_digit:], True
    return snailfish, False


def addition(snailfish_1, snailfish_2):
    return f"[{snailfish_1},{snailfish_2}]"


def reduce(snailfish):
    while True:
        snailfish, exploded = explode(snailfish)
        if exploded:
            continue
        snailfish, splitted = split(snailfish)
        if splitted:
            continue
        return snailfish


def sum(snailfishes):
    while len(snailfishes) > 1:
        snailfish_1 = snailfishes.pop(0)
        snailfish_2 = snailfishes.pop(0)
        snailfish = reduce(addition(snailfish_1, snailfish_2))
        snailfishes.insert(0, snailfish)
    return snailfish


def magnitude(snailfish):
    pos_comma = last_magnitude = 0
    while True:
        pos_comma = snailfish.find(",", pos_comma + 1)
        if pos_comma == -1:
            return last_magnitude
        if snailfish[pos_comma - 1].isdigit() and snailfish[pos_comma + 1].isdigit():
            pos_opened = snailfish.rfind("[", 0, pos_comma)
            pos_closed = snailfish.find("]", pos_comma)
            last_magnitude = int(snailfish[pos_opened + 1:pos_comma]) * 3 + int(snailfish[pos_comma + 1:pos_closed]) * 2
            snailfish = snailfish[:pos_opened] + str(last_magnitude) + snailfish[pos_closed + 1:]
            pos_comma = 0


def homework(data):
    return magnitude(sum(data.strip().split("\n")))


def solve1(data):
    return homework(data)


def solve2(data):
    snailfishes = data.strip().split("\n")
    max_magnitude = 0
    for snailfish_1, snailfish_2 in itertools.permutations(snailfishes, 2):
        this_magnitude = magnitude(sum([snailfish_1, snailfish_2]))
        if this_magnitude > max_magnitude:
            max_magnitude = this_magnitude
    return max_magnitude


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
