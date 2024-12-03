import re


def mul(data: str, do_dont: bool = False) -> int:
    total = 0
    do = True
    for found in re.findall(r"mul\(\d{1,3},\s*\d{1,3}\)|do\(\)|don't\(\)", data):
        if found in ("do()", "don't()"):
            do = found == "do()"
        elif do or not do_dont:
            x, y = [int(a) for a in found.split("(")[1].split(")")[0].split(",")]
            total += x * y
    return total


def solve1(data: str) -> int:
    return mul(data)


def solve2(data: str) -> int:
    return mul(data, True)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
