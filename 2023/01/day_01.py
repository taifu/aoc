from operator import gt, lt


def load(data):
    return data.strip().split("\n")


def firstlastdigit(line):
    first = last = None
    for pos, c in enumerate(line):
        if c.isdigit():
            if first is None:
                first = last = (c, pos)
            else:
                last = (c, pos)
    return first, last


def count(lines):
    tot = 0
    codes = []
    for line in lines:
        first, last = firstlastdigit(line)
        tot += int(first[0] + last[0])
        codes.append(int(first[0] + last[0]))
    return tot


def solve1(data):
    return count(load(data))


def solve2(data):
    lines = load(data)
    for n, line in enumerate(lines):
        for op, find, get_posdigit in ((gt, "index", 0), (lt, "rindex", 1)):
            posdigit = firstlastdigit(line)[get_posdigit]
            found = None
            for digit, spell in enumerate(("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")):
                digit += 1
                try:
                    pos = getattr(line, find)(spell)
                    if found is None or op(found[0], pos):
                        found = (pos, digit, spell)
                except ValueError:
                    continue
            if found and not (posdigit and op(found[0], posdigit[1])):
                pos, digit, spell = found
                lines[n] = line = line[:pos] + str(digit) + line[pos + len(spell):]
    return count(lines)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
    print(solve2("oneight"))
