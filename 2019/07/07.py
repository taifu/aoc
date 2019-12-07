from itertools import permutations


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
        self.input = input

    def run(self):
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


class Amplifier:
    def __init__(self, program):
        self.program = program

    def find_max(self):
        computer = Computer(self.program)
        max_output = (0, None)
        for sequence in permutations(range(5)):
            next_input = 0
            for step in sequence:
                computer.reset(input=[step, next_input])
                computer.run()
                next_input = computer.output[0]
            if next_input > max_output[0]:
                max_output = (next_input, sequence)
        return max_output

    def find_max_loop(self):
        max_output = (0, None)
        for sequence in permutations(range(5, 10)):
            computers = [Computer(self.program) for n in range(5)]
            next_input = 0
            n = loop = 0
            while True:
                loop += 1
                n = n % 5
                computer = computers[n]
                if not computer.started:
                    step = sequence[n]
                    computer.reset(input=[step, next_input])
                else:
                    computer.input.append(next_input)
                try:
                    computer.run()
                    next_input = computer.output.pop(0)
                    if n == 4:
                        break
                except StopException:
                    next_input = computer.output.pop(0)
                n += 1
            if next_input > max_output[0]:
                max_output = (next_input, sequence)
        return max_output


def test_p1():
    amps = Amplifier("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")
    assert amps.find_max() == (43210, (4, 3, 2, 1, 0))


def test_p2():
    amps = Amplifier("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")
    assert amps.find_max() == (54321, (0, 1, 2, 3, 4))


def test_p3():
    amps = Amplifier("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")
    assert amps.find_max() == (65210, (1, 0, 4, 3, 2))


def test_p4():
    amps = Amplifier("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
    assert amps.find_max_loop() == (139629729, (9, 8, 7, 6, 5))


def test_p5():
    amps = Amplifier("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")
    assert amps.find_max_loop() == (18216, (9, 7, 8, 5, 6))


if __name__ == "__main__":
    amps = Amplifier(open('input.txt').read())
    print(amps.find_max()[0])
    print(amps.find_max_loop()[0])
