def load(data):
    rows = data.split("\n")
    numbers = tuple(int(c) for c in rows[0].split(","))
    boards = []
    for n, row in enumerate(rows[1:]):
        if n % 6 == 0:
            board = []
        else:
            board.append([[int(c), False] for c in row.split(" ") if c])
            if n % 6 == 5:
                boards.append(board)
    return numbers, boards


def left(board):
    numbers = []
    for line in board:
        for n, drawn in line:
            if drawn == 0:
                numbers.append(n)
    return numbers


def mark(number, boards):
    for board in boards:
        for line in board:
            for n_drawn in line:
                if n_drawn[0] == number:
                    n_drawn[1] = True


def check(board):
    for n, line in enumerate(board):
        if all(n_drawn[1] for n_drawn in line):
            return board
        if all(line[n][1] for line in board):
            return board


def draw(numbers, boards, last=False):
    for number in numbers:
        mark(number, boards)
        left_boards = []
        for board in boards:
            if check(board):
                if not last:
                    return number, board
            else:
                left_boards.append(board)
        if last:
            if len(left_boards) == 0:
                return number, board
            boards = left_boards


def solve1(data):
    numbers, boards = load(data)
    number, board = draw(numbers, boards)
    return number * sum(left(board))


def solve2(data):
    numbers, boards = load(data)
    number, board = draw(numbers, boards, last=True)
    return number * sum(left(board))


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
