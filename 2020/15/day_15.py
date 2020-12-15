def parse(numbers, data):
    lasts = {}
    for i, p in enumerate(data.strip().split(",")):
        last = int(p)
        numbers[i] = last
        lasts[last] = (i + 1,)
    return lasts, last, len(lasts)


def solve(data, n=2020):
    numbers = [None] * n
    lasts, last, turns = parse(numbers, data)
    while True:
        last = 0 if len(lasts[last]) == 1 else turns - lasts[last][-2]
        numbers[turns] = last
        turns += 1
        try:
            lasts[last] = (lasts[last][-1], turns)
        except KeyError:
            lasts[last] = (turns,)
        if turns == n:
            return last


if __name__ == "__main__":
    data = "0,13,1,8,6,15"
    print(solve(data))
    print(solve(data, n=30000000))
