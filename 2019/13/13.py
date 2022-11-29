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


class Game:
    def __init__(self, output):
        self.screen = dict(((x, y), t) for x, y, t in zip(*(iter(output),) * 3))
        self.score = self.screen.pop((-1, 0), 0)
        self.width = max(x for x, y in self.screen.keys()) + 1
        self.height = max(y for x, y in self.screen.keys()) + 1

    def paint(self):
        print("\033[0;0H")
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                tile = self.screen.get((x, y), 0)
                if tile == 0:
                    row += " "
                elif tile == 1:
                    row += "#"
                elif tile == 2:
                    row += "x"
                elif tile == 3:
                    row += "_"
                    self.player = x
                elif tile == 4:
                    row += "o"
                    self.ball = x
                else:
                    raise Exception("Tile unknown {} at {},{}".format(tile, x, y))
            print(row)
        print("Score: {}".format(self.score))


if __name__ == "__main__":
    c = Computer(open('input.txt').read())
    c.run(input=0, reset=True)
    g = Game(c.output)
    g.paint()
    part1 = sum(1 for t in g.screen.values() if t == 2)
    c.reset()
    c.program[0] = 2
    stop = False
    print("\033[2J")
    while not stop:
        try:
            c.run()
            stop = True
        except StopException:
            pass
        g = Game(c.output)
        g.paint()
        if g.ball > g.player:
            c.set_input(1)
        elif g.ball < g.player:
            c.set_input(-1)
        else:
            c.set_input(0)
        #time.sleep(0.05)
    print(part1)
    print(g.score)
