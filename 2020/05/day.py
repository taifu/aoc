from collections import defaultdict


def calc(strip, low):
    s = 2**len(strip)
    f, t = 0, s - 1
    for c in strip:
        s /= 2
        if c == low:
            t -= s
        else:
            f += s
    return int(t)


def fill(data):
    seats = defaultdict(list)
    max_id = 0
    for line in data.strip().split('\n'):
        row = calc(line[:7], 'F')
        col = calc(line[7:], 'L')
        seats[row].append(col)
        max_id = max(max_id, row * 8 + col)
    return max_id, seats


if __name__ == "__main__":
    data = open("input.txt").read()
    max_id, seats = fill(data)
    print(max_id)
    for n, (row, cols) in enumerate(sorted(seats.items())):
        if n == 0:
            continue
        if len(cols) < 8:
            print(row * 8 + (set(range(8)) - set(cols)).pop())
            break
