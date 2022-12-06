def message(data, length):
    for x in range(length, len(data)):
        if len(set(data[x - length:x])) == length:
            return x

def solve1(data):
    return message(data, 4)


def solve2(data):
    return message(data, 14)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
