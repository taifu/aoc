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


def test_programs():
    c = Computer("1002,4,3,4,33")
    c.run(1)
    assert c.program == {0: 1002, 1: 4, 2: 3, 3: 4, 4: 99}

    c = Computer("3,9,8,9,10,9,4,9,99,-1,8")
    c.run(8)
    assert c.output == [1]
    c.run(9)
    assert c.output == [0]

    c = Computer("3,9,7,9,10,9,4,9,99,-1,8")
    c.run(7)
    assert c.output == [1]
    c.run(9)
    assert c.output == [0]

    c = Computer("3,3,1108,-1,8,3,4,3,99")
    c.run(8)
    assert c.output == [1]
    c.run(9)
    assert c.output == [0]

    c = Computer("3,3,1107,-1,8,3,4,3,99")
    c.run(7)
    assert c.output == [1]
    c.run(9)
    assert c.output == [0]

    program = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    c = Computer(program)
    c.run()
    assert c.output == [int(n) for n in program.split(",")]

    program = "1102,34915192,34915192,7,4,7,99,0"
    c = Computer(program)
    c.run()
    assert len(str(c.output.pop())) == 16  # 1219070632396864

    program = "104,1125899906842624,99"
    c = Computer(program)
    c.run()
    assert c.output.pop() == int(program.split(",")[1])


if __name__ == "__main__":
    c = Computer(open('input.txt').read())
    c.run(1)
    print(c.output.pop())
    c.reset()
    c.run(2)
    print(c.output.pop())
