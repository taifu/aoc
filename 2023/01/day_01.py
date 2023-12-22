from typing import TypeAlias


Lines: TypeAlias = list[str]


def load(data: str) -> Lines:
    return data.splitlines()


def count(lines: Lines, spelt: bool = False) -> int:
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


def solve1(data: str) -> int:
    return count(load(data))


def solve2(data: str) -> int:
    return count(load(data), True)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
