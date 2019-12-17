import time
from collections import defaultdict


class StopException(Exception):
    pass


class Computer:
    def op_add(self, value1, value2):
        return value1 + value2

    def op_mul(self, value1, value2):
        return value1 * value2

    def op_input(self):
        if not self.input:
            raise StopException
        return self.input.pop(0)

    def op_output(self, value):
        self.output.append(value)

    def op_jump_true(self, value, pointer):
        if value != 0:
            self.pos = pointer

    def op_jump_false(self, value, pointer):
        if value == 0:
            self.pos = pointer

    def op_less_than(self, value1, value2):
        if value1 < value2:
            return 1
        return 0

    def op_equals(self, value1, value2):
        if value1 == value2:
            return 1
        return 0

    def op_adjust_relative(self, value):
        self.relative_base += value

    def __init__(self, program: str):
        self.program = defaultdict(int)
        for n, c in enumerate(program.split(',')):
            self.program[n] = int(c.strip())
        self._backup = self.program.copy()
        self.started = False
        self.lang = {1: (2, 1, self.op_add),
                     2: (2, 1, self.op_mul),
                     3: (0, 1, self.op_input),
                     4: (1, 0, self.op_output),
                     5: (2, 0, self.op_jump_true),
                     6: (2, 0, self.op_jump_false),
                     7: (2, 1, self.op_less_than),
                     8: (2, 1, self.op_equals),
                     9: (1, 0, self.op_adjust_relative),
                     }
        self.reset()

    def reset(self):
        self.started = True
        self.program = self._backup.copy()
        self.output = []
        self.pos = 0
        self.relative_base = 0
        self.input = []

    def set_input(self, input=None):
        if input is not None:
            if not isinstance(input, list):
                input = [input]
            self.input = input
        else:
            self.input = []

    def run(self, input=None, reset=False):
        if reset:
            self.reset()
        if input is not None:
            self.set_input(input)
        while True:
            parameters_mode, opcode = ('000' + str(self.program[self.pos] // 100))[-3:], self.program[self.pos] % 100
            if opcode == 99:
                break
            parameters_input, parameters_output, operator = self.lang[opcode]
            tot_parameters = parameters_input + parameters_output
            parameters = []
            for n in range(parameters_input):
                parameter = self.program[self.pos + 1 + n]
                parameter_mode = parameters_mode[2 - n]
                if parameter_mode == '2':  # Relative mode (the value stored at value position + relative base)
                    parameter = self.program[parameter + self.relative_base]
                elif parameter_mode == '0':  # Position mode (the value stored at value position)
                    parameter = self.program[parameter]
                elif parameter_mode != '1':  # Immediate (the value)
                    raise Exception("Unexpected parameter mode: {}".format(parameter_mode))
                parameters.append(parameter)
            if parameters_output:
                assert parameters_output == 1
                parameter_mode = parameters_mode[2 - parameters_input]
                pos_output = self.program[self.pos + tot_parameters]
                if parameter_mode == '2':  # Relative mode (the value stored at value position + relative base)
                    pos_output += self.relative_base
            old_pos = self.pos
            result = operator(*parameters)
            if old_pos == self.pos:
                self.pos += tot_parameters + 1
            if parameters_output:
                self.program[pos_output] = result


SCAFFOLD = "#"
DIRECTIONS = {"v": 0, "<": 1, "^": 2, ">": 3}
DELTA = {DIRECTIONS["v"]: (0, 1), DIRECTIONS["^"]: (0, -1), DIRECTIONS["<"]: (-1, 0), DIRECTIONS[">"]: (1, 0)}


if __name__ == "__main__":
    computer = Computer(open('input.txt').read())
    computer.run()
    output = "".join(chr(c) for c in computer.output)
    print(output)
    outside = [row.strip() for row in output.strip().split("\n")]
    width = len(outside[0])
    height = len(outside)
    intersections = set()
    position = None
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if outside[y][x] in DIRECTIONS:
                position = (x, y)
                direction = DIRECTIONS[outside[y][x]]
            if outside[y][x] == outside[y + 1][x] == outside[y - 1][x] == outside[y][x + 1] == outside[y][x - 1] == SCAFFOLD:
                intersections.add((x, y))
    print(sum((x * y) for x, y in intersections))
    movements = []
    step = turns = 0
    while True:
        delta = DELTA[direction]
        wrong = False
        try:
            next_position = (position[0] + delta[0], position[1] + delta[1])
            if outside[next_position[1]][next_position[0]] == SCAFFOLD:
                if turns:
                    if step:
                        movements.append(str(step))
                    step = 0
                    if turns == 3:
                        movements.append("L")
                    elif turns == 1:
                        movements.append("R")
                    else:
                        raise Exception("Wrong turns {}".format(turns))
                    turns = 0
                step += 1
                position = next_position
            else:
                wrong = True
        except IndexError:
            wrong = True
        if wrong:
            if turns == 4:
                movements.append(str(step))
                break
            while True:
                direction = (direction + 1) % 4
                turns += 1
                if turns != 2:
                    break
    print(",".join(movements))
    # L,12,L,12,L,6,L,6,R,8,R,4,L,12,L,12,L,12,L,6,L,6,L,12,L,6,R,12,R,8,R,8,R,4,L,12,L,12,L,12,L,6,L,6,L,12,L,6,R,12,R,8,R,8,R,4,L,12,L,12,L,12,L,6,L,6,L,12,L,6,R,12,R,8
    # Brutal search!
    tot_move = len(movements)
    solutions = []
    for l1 in range(2, 20, 2):
        A = B = C = None
        movements_try_a = movements[:]
        A, movements_try_a = movements_try_a[:l1], movements_try_a[l1:]
        moves_a = [A]
        while movements_try_a[:l1] == A:
            movements_try_a = movements_try_a[l1:]
            moves_a.append(A)
        for l2 in range(2, 20, 2):
            movements_try_b = movements_try_a[:]
            moves_b = moves_a[:]
            B, movements_try_b = movements_try_b[:l2], movements_try_b[l2:]
            moves_b.append(B)
            while movements_try_b[:l1] == A or movements_try_b[:l2] == B:
                if movements_try_b[:l1] == A:
                    movements_try_b = movements_try_b[l1:]
                    moves_b.append(A)
                else:
                    movements_try_b = movements_try_b[l2:]
                    moves_b.append(B)
            for l3 in range(2, 20, 2):
                movements_try_c = movements_try_b[:]
                moves_c = moves_b[:]
                C, movements_try_c = movements_try_c[:l3], movements_try_c[l3:]
                moves_c.append(C)
                while movements_try_c[:l1] == A or movements_try_c[:l2] == B or movements_try_c[:l3] == C:
                    if movements_try_c[:l1] == A:
                        movements_try_c = movements_try_c[l1:]
                        moves_c.append(A)
                    elif movements_try_c[:l2] == B:
                        movements_try_c = movements_try_c[l2:]
                        moves_c.append(B)
                    else:
                        movements_try_c = movements_try_c[l3:]
                        moves_c.append(C)
                if not movements_try_c:
                    assert([m for sublist in moves_c for m in sublist] == movements)
                    solutions.append(moves_c)

    for solution in solutions:
        # X,X,X,X,X,X,X,X,X,X -> max 10 moves
        if len(solution) <= 10:
            for item in solution:
                if len(",".join(str(c) for c in item)) > 20:
                    break
            else:
                moves = []
                found = {}
                steps = []
                name = ord('A')
                for item in solution:
                    move = ",".join(str(c) for c in item)
                    if move not in found:
                        move_name = chr(name + len(found))
                        found[move] = move_name
                        steps.append(move)
                    moves.append(found[move])
                print("Found!")
                break

    # L,12,L,12,L,6,L,6,R,8,R,4,L,12,L,12,L,12,L,6,L,6,L,12,L,6,R,12,R,8,R,8,R,4,L,12,L,12,L,12,L,6,L,6,L,12,L,6,R,12,R,8,R,8,R,4,L,12,L,12,L,12,L,6,L,6,L,12,L,6,R,12,R,8
    """
    A,B,A,C,B,A,C,B,A,C
    A = L,12,L,12,L,6,L,6
    B = R,8,R,4,L,12
    A = L,12,L,12,L,6,L,6
    C = L,12,L,6,R,12,R,8
    B = R,8,R,4,L,12
    A = L,12,L,12,L,6,L,6
    C = L,12,L,6,R,12,R,8
    B = R,8,R,4,L,12
    A = L,12,L,12,L,6,L,6
    C = L,12,L,6,R,12,R,8
    """
    program_by_hand = ["A,B,A,C,B,A,C,B,A,C", "L,12,L,12,L,6,L,6", "R,8,R,4,L,12", "L,12,L,6,R,12,R,8"]
    program = [",".join(m for m in moves)] + steps
    assert program == program_by_hand
    computer.reset()
    assert computer.program[0] == 1
    computer.program[0] = 2
    computer.set_input([ord(c) for c in "\n".join(program + [""]) + "y\n"])
    print("".join(chr(c) for c in computer.input))
    computer.run()
    answer = computer.output.pop()
    output = "".join(chr(c) for c in computer.output)
    print("\033[2J")
    for n, frame in enumerate(output.split("\n")[height + 7:]):
        if n % (height + 1) == 0:
            time.sleep(0.03)
            print("\033[0;0H")
        print(frame)
    print()
    print("\033[{};0H".format(str(height + 2)))
    print(sum((x * y) for x, y in intersections))
    print(answer)
