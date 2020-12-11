from collections import defaultdict


FLOOR, OCCUPIED, EMPTY = '.', '#', 'L'


def parse(data):
    seats = []
    for line in data.strip().split('\n'):
        seats.append(list(line))
    return seats


def solve(data, step=1):
    assert step in (1, 2)
    seats = parse(data)
    max_adiacent = 4 if step == 1 else 5
    while True:
        new_seats = []
        changed = occupied = 0
        for row, line in enumerate(seats):
            new_line = []
            for col, pos in enumerate(line):
                if pos == FLOOR:
                    new_line.append(pos)
                    continue
                adiacent = 0
                if step == 1:
                    for a_row in range(row - 1, row + 2):
                        if a_row >= 0 and a_row < len(seats):
                            for a_col in range(col - 1, col + 2):
                                if a_col >= 0 and a_col < len(line) and not (a_row == row and a_col == col):
                                    adiacent += 1 if seats[a_row][a_col] == OCCUPIED else 0
                else:
                    for d_x in (-1, 0, 1):
                        for d_y in (-1, 0, 1):
                            if d_x != 0 or d_y != 0:
                                new_row, new_col = row, col
                                while True:
                                    new_row += d_x
                                    if new_row < 0 or new_row >= len(seats):
                                        break
                                    new_col += d_y
                                    if new_col < 0 or new_col >= len(line):
                                        break
                                    if seats[new_row][new_col] in (OCCUPIED, EMPTY):
                                        adiacent += 1 if seats[new_row][new_col] == OCCUPIED else 0
                                        break
                if pos == EMPTY:
                    if adiacent == 0:
                        new_line.append(OCCUPIED)
                        changed += 1
                        occupied += 1
                    else:
                        new_line.append(EMPTY)
                elif pos == OCCUPIED:
                    if adiacent >= max_adiacent:
                        new_line.append(EMPTY)
                        changed += 1
                    else:
                        new_line.append(OCCUPIED)
                        occupied += 1
            new_seats.append(new_line)
        if changed == 0:
            return occupied
        seats = new_seats


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, step=2))
