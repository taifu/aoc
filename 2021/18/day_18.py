import re
import itertools


def explode(snailfish):
    opened = 0
    for pos_opened, c in enumerate(snailfish):
        opened += 1 if c == '[' else -1 if c == ']' else 0
        if opened >= 5 and (pair_match := re.match(r'^(\d+,\d+).*$', snailfish[pos_opened + 1:])):
            pair = pair_match.group(1)
            pos_closed = pos_opened + len(pair) + 2
            left, right = snailfish[:pos_opened], snailfish[pos_closed:]
            n1, n2 = (int(p) for p in pair.split(','))
            if (last_digit := re.match(r'(.*)(?<!\d)(\d+)([^\d]*)$', left)) is not None:
                left = last_digit.group(1) + str(n1 + int(last_digit.group(2))) + last_digit.group(3)
            if (first_digit := re.match(r'([^\d]+)(\d+)(.*)$', right)) is not None:
                right = first_digit.group(1) + str(n2 + int(first_digit.group(2))) + first_digit.group(3)
            return left + "0" + right, True
    return snailfish, False


def split(snailfish):
    return re.subn(r'(\d{2,})', lambda number: f"[{int(number.group())//2},{(int(number.group()) + 1)//2}]", snailfish, 1)


def reduce(snailfish):
    while True:
        for op in explode, split:
            snailfish, done = op(snailfish)
            if done:
                break
        else:
            return snailfish


def sum(snailfishes):
    while len(snailfishes) > 1:
        snailfishes = [reduce(f"[{snailfishes[0]},{snailfishes[1]}]")] + snailfishes[2:]
    return snailfishes[0]


def magnitude(snailfish):
    while True:
        snailfish, n = re.subn(r'\[(\d+),(\d+)\]', lambda pair: str(int(pair.group(1)) * 3 + int(pair.group(2)) * 2), snailfish)
        if n == 0:
            return int(snailfish)


def solve1(data):
    return magnitude(sum(data.strip().split("\n")))


def solve2(data):
    snailfishes = data.strip().split("\n")
    max_magnitude = 0
    for snailfish_1, snailfish_2 in itertools.permutations(snailfishes, 2):
        if (this_magnitude := magnitude(sum([snailfish_1, snailfish_2]))) > max_magnitude:
            max_magnitude = this_magnitude
    return max_magnitude


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
