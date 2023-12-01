def load(data):
    return data.strip().split("\n")


def count(lines, spelt=False):
    tot = 0
    for line in lines:
        digits = []
        for n, c in enumerate(line):
            if c.isdecimal():
                digits.append(int(c))
            elif spelt:
                for digit, spell in enumerate(("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")):
                    if line[n:].startswith(spell):
                        digits.append(digit + 1)
                        break
        tot += digits[0] * 10 + digits[-1]
    return tot


def solve1(data):
    return count(load(data))


def solve2(data):
    return count(load(data), True)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
    print(solve2("oneight"))
