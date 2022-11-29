import operator


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

    def __init__(self, program: str):
        self.program = [int(c.strip()) for c in program.split(',')]
        self._backup = self.program[:]
        self.started = False
        self.lang = {1: (2, 1, self.op_add),
                     2: (2, 1, self.op_mul),
                     3: (0, 1, self.op_input),
                     4: (1, 0, self.op_output),
                     5: (2, 0, self.op_jump_true),
                     6: (2, 0, self.op_jump_false),
                     7: (2, 1, self.op_less_than),
                     8: (2, 1, self.op_equals),
                     }

    def reset(self, input, pos=0):
        self.started = True
        self.program = self._backup[:]
        self.output = []
        self.pos = pos
        if not isinstance(input, list):
            input = [input]
        self.input = input

    def run(self, input=None):
        if input:
            self.reset(input)
        while True:
            parameters_mode, opcode = ('000' + str(self.program[self.pos] // 100))[-3:], self.program[self.pos] % 100
            if opcode == 99:
                break
            parameters_input, parameters_output, operator = self.lang[opcode]
            tot_parameters = parameters_input + parameters_output
            parameters = []
            for n in range(parameters_input):
                parameter = self.program[self.pos + 1 + n]
                if parameters_mode[2 - n] == '0':
                    parameter = self.program[parameter]
                parameters.append(parameter)
            old_pos = self.pos
            result = operator(*parameters)
            if old_pos == self.pos:
                self.pos += tot_parameters + 1
            if parameters_output:
                self.program[self.program[self.pos - 1]] = result


def test_programs():
    c = Computer("1002,4,3,4,33")
    c.run(1)
    assert c.program == [1002, 4, 3, 4, 99]

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

    c = Computer("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")
    c.run(7)
    assert c.output == [999]
    c.run(8)
    assert c.output == [1000]
    c.run(9)
    assert c.output == [1001]


if __name__ == "__main__":
    c = Computer(open('input.txt').read())
    c.run(1)
    print(c.output[-1])
    c.run(5)
    print(c.output[-1])
