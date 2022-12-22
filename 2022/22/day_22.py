from operator import mul, truediv


LEFT, RIGHT = 'L', 'R'
OPEN, WALL = '.', '#'
TURN_RIGHT, TURN_LEFT = lambda x: mul(x, 1j), lambda x: truediv(x, 1j)


def load(data):
    board = {}
    part0, path = data.split("\n\n")
    # Topmost, leftmost = 1, 1
    for y, line in enumerate(part0.split('\n')):
        for x, char in enumerate(line):
            if char in OPEN + WALL:
                board[x + 1j * y] = char
    moves = []
    while True:
        first_r = (path + RIGHT).index(RIGHT)
        first_l = (path + LEFT).index(LEFT)
        pos = min(first_r, first_l)
        moves.append(int(path[:pos if pos else len(path)]))
        if pos == len(path):
            break
        moves.append(TURN_RIGHT if path[pos] == RIGHT else TURN_LEFT)
        path = path[pos + 1:]
    return board, moves


class Board:
    def __init__(self, board, cube):
        self.board = board
        self.cube = cube
        self.current = 0
        self.direction = 1
        self.max_x = max(p.real for p in self.board)
        self.max_y = max(p.imag for p in self.board)
        if self.cube:
            import pdb; pdb.set_trace()
            self.width = int(self.max_x + 1)/4
        while not self.current in self.board:
            self.current += 1

    def wrap(self, position):
        starting, direction = position, self.direction
        #if (starting, direction) == ((11+5j), (1+0j)):
            #import pdb; pdb.set_trace()
        if self.cube:
            position += direction
            if direction == 1:
                if position.imag < self.width:
                    assert position.real == self.width * 3, "impossible real position"
                    direction = -1
                    position = (self.width * 4 - 1) + 1j * (self.width * 3 - position.imag - 1)
                elif position.imag < 2 * self.width:
                    assert position.real == self.width * 3, "impossible real position"
                    direction = 1j
                    position = (self.width * 5 - 1 - position.imag) + 1j * (self.width * 2)
                elif position.imag < 3 * self.width:
                    assert position.real == self.width * 4, "impossible real position"
                    direction = -1
                    position = (self.width * 3 - 1) + 1j * (-self.width * 3 + position.imag + 1)
                else:
                    assert False, "impossible position"
            elif direction == -1:
                if position.imag < self.width:
                    assert position.real == self.width * 2 - 1, "impossible real position"
                    direction = 1j
                    position = (self.width + position.imag) + 1j * (self.width + 1)
                elif position.imag < 2 * self.width:
                    assert position.real == - 1, "impossible real position"
                    direction = -1j
                    position = (self.width * 5 - 1 - position.imag) + 1j * (self.width * 3 - 1)
                elif position.imag < 3 * self.width:
                    assert position.real == self.width * 2 - 1, "impossible real position"
                    direction = -1j
                    position = (self.width * 4 - 1 - position.imag) + 1j * (self.width * 2 - 1)
                else:
                    assert False, "impossible position"
            elif direction == 1j:
                if position.real < self.width:
                    assert position.imag == self.width * 2, "impossible imag position"
                    direction = -1j
                    position = (self.width * 3 - 1 - position.real) + 1j * (self.width * 3 - 1)
                elif position.real < 2 * self.width:
                    assert position.imag == self.width * 2, "impossible imag position"
                    direction = 1
                    position = self.width * 2 + 1j * (self.width * 4 - 1 - position.real)
                elif position.real < 3 * self.width:
                    assert position.imag == self.width * 3, "impossible imag position"
                    direction = -1j
                    position = self.width * 3 - 1 - position.real + 1j * (self.width * 2 - 1)
                elif position.real < 4 * self.width:
                    assert position.imag == self.width * 3, "impossible imag position"
                    direction = 1
                    position = 0 + 1j * (self.width * 4 -1 - position.real)
                else:
                    assert False, "impossible position"
            elif direction == -1j:
                if position.real < self.width:
                    assert position.imag == self.width - 1, "impossible imag position"
                    direction = 1j
                    position = self.width * 3 - 1 - position.real + 1j * (0)
                elif position.real < 2 * self.width:
                    assert position.imag == self.width - 1, "impossible imag position"
                    direction = 1
                    position = self.width * 2 + 1j * (position.real - self.width)
                elif position.real < 3 * self.width:
                    assert position.imag == -1, "impossible imag position"
                    direction = 1j
                    position = self.width * 3 - 1 - position.real + 1j * (self.width - 1)
                elif position.real < 4 * self.width:
                    assert position.imag == self.width * 2 - 1, "impossible imag position"
                    direction = -1
                    position = self.width * 3 - 1 + 1j * (self.width * 4 - 1 - position.real)
                else:
                    assert False, "impossible position"
            assert position in self.board, "outside position"
            while True:
                if position in self.board:
                    if self.board[position] == OPEN:
                        self.direction = direction
                        return position
                    return starting
                position += direction
        else:
            if direction == 1:
                position = -1 + 1j * position.imag
            elif direction == -1:
                position = self.max_x + 1 + 1j * position.imag
            elif direction == 1j:
                position = position.real -1j
            else:
                position = position.real + 1j * (self.max_y + 1)
            while True:
                position += direction
                if position in self.board:
                    if self.board[position] == OPEN:
                        return position
                    return starting

    def draw(self):
        for y in range(40):
            line = ""
            for x in range(50):
                position = x + 1j * y
                try:
                    char = self.board[position]
                    if position == self.current:
                        char = {1: '>', -1: '<', 1j: 'v', -1j: '^'}[self.direction]
                    line += char
                except KeyError:
                    line += " "
            print(line)

    def move(self, move):
        if not isinstance(move, int):
            self.direction = move(self.direction)
            return
        while move:
            next_current = self.current + self.direction
            if next_current not in self.board:
                next_current = self.wrap(self.current)
                # WALL
                if next_current == self.current:
                    break
            elif self.board[next_current] == WALL:
                break
            self.current = next_current
            move -= 1


def password(data, cube=False):
    grid, moves = load(data)
    board = Board(grid, cube=cube)
    for move in moves:
        board.move(move)
    return int(1000 * (board.current.imag + 1) + 4 * (board.current.real + 1) + {1: 0, 1j: 1, -1: 2, -1j: 3}[board.direction])


def solve1(data):
    return password(data)


def solve2(data):
    return password(data, cube=True)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
