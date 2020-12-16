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


def row_col(line):
    row = calc(line[:7], 'F')
    col = calc(line[7:], 'L')
    return row, col


def calc_id(row, col):
    return row * 8 + col


def solve1(data):
    seats = defaultdict(list)
    max_id = 0
    for line in data.strip().split('\n'):
        row, col = row_col(line)
        seats[row].append(col)
        max_id = max(calc_id(row, col), max_id)
    return max_id, seats


def solve2(seats):
    for n, (row, cols) in enumerate(sorted(seats.items())):
        if n == 0:
            continue
        if len(cols) < 8:
            return(calc_id(row, (set(range(8)) - set(cols)).pop()))
            break


if __name__ == "__main__":
    data = open("input.txt").read()
    max_id, seats = solve1(data)
    print(max_id)
    print(solve2(seats))
