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


class Area:
    def __init__(self, computer):
        self.computer = computer

    def scan(self, width, height, start_x=0, start_y=0):
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.map = {}
        for x in range(self.start_x, self.width):
            for y in range(self.start_y, self.height):
                self.computer.reset()
                self.computer.set_input([x, y])
                self.computer.run()
                self.map[(x, y)] = self.computer.output.pop()
        self.rows = []
        for y in range(self.start_y, self.height):
            row = []
            for x in range(self.start_x, self.width):
                row.append('#' if self.map[(x, y)] == 1 else '.' if self.map[(x, y)] == 0 else '?')
            self.rows.append("".join(row))

    def show(self):
        for y in range(self.start_y, self.height):
            row = []
            for x in range(self.start_x, self.width):
                row.append('#' if self.map[(x, y)] == 1 else '.' if self.map[(x, y)] == 0 else '?')
            print("".join(row))

    def count(self):
        return sum(1 if self.map[(x, y)] == 1 else 0 for x in range(self.start_x, self.width) for y in range(self.start_y, self.height))

    def intercept(self, square):
        ship = '#' * square
        for y, row in enumerate(self.rows):
            x = row.find(ship)
            if x >= 0:
                found = False
                dx = 0
                while not found:
                    if x + dx + square == self.width or row[x + dx:x + dx + square] != ship:
                        break
                    if y + square == self.height:
                        break
                    for dy in range(y, y + square):
                        if self.rows[dy][x + dx:x + dx + square] != ship:
                            break
                    else:
                        found = True
                        break
                    dx += 1
                if found:
                    return (x + dx + self.start_x) * 10000 + y + self.start_y
        return None


if __name__ == "__main__":
    computer = Computer(open('input.txt').read())
    area = Area(computer)
    area.scan(50, 50)
    area.show()
    print(area.count())
    size = 1100
    start_x = 750
    start_y = 750
    print("Please, wait a minute while I'm scanning a {0} by {0} map. Thank you :-)".format(size))
    area.scan(size, size, start_x, start_y)
    print(area.intercept(100))
