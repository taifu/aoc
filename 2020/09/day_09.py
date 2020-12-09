def check(n, numbers):
    for i, n1 in enumerate(numbers[:-1]):
        for n2 in numbers[i + 1:]:
            if n1 + n2 == n:
                return True
    return False


def parse(data):
    return [int(x) for x in data.strip().split("\n")]


def solve2(data, value):
    numbers = parse(data)
    for n in range(2, len(numbers)):
        for pos in range(1, len(numbers) - n):
            if sum(numbers[pos:pos + n]) == value:
                return(min(numbers[pos:pos + n]) + max(numbers[pos:pos + n]))


def solve(data, preamble):
    numbers = parse(data)
    pos = preamble
    while True:
        if not check(numbers[pos], numbers[pos - preamble:pos]):
            return numbers[pos]
        pos += 1


if __name__ == "__main__":
    data = open("input.txt").read()
    n = solve(data, 25)
    print(n)
    print(solve2(data, n))
