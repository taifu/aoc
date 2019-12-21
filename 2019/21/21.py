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


def explore(computer, program, end="WALK"):
    computer.reset()
    computer.set_input([ord(c) for c in program + "\n{}\n".format(end)])
    computer.run()
    output = ""
    ok = False
    for c in computer.output:
        try:
            output += chr(c)
        except ValueError:
            ok = True
            output += str(c)
    return output, ok


def solve(program=[], end="WALK", stop=True, extra=False, max_n=5):
    def generate():
        instructions = set(["AND {} {}", "OR {} {}", "NOT {} {}"])
        ops1 = set("ABCDTJ")
        if extra:
            ops1 |= set("EFGHI")
        ops2 = set("TJ")
        vars = []
        for instruction in instructions:
            for op1 in ops1:
                for op2 in ops2:
                    vars.append(instruction.format(op1, op2))
        return vars
    ALL = generate()
    tot = len(ALL)
    ok = False
    program_start = program[:]
    for n in range(1, max_n + 1):
        print("Step {}".format(n))
        counters = [0] * n
        finish = False
        while not finish:
            program = "\n".join(program_start + [ALL[counters[i]] for i in range(n)])
            if all(program.count(" " + c) <= 1 for c in "ABCDEFGHI"):
                output, ok = explore(computer, program, end)
            else:
                output = ok = False
            if ok:
                print(program)
                print(output)
                if stop:
                    finish = True
                    break
            i = 0
            while i < n:
                counters[i] += 1
                if counters[i] < tot:
                    break
                counters[i] = 0
                i += 1
            finish = (i == n)
        if ok:
            break


if __name__ == "__main__":
    # AND X Y sets Y to true if both X and Y are true; otherwise, it sets Y to false.
    # OR X Y sets Y to true if at least one of X or Y is true; otherwise, it sets Y to false.
    # NOT X Y sets Y to true if X is false; otherwise, it sets Y to false.
    computer = Computer(open('input.txt').read())
    # Simple program:
    program = """NOT A J"""
    #   #####.#..########
    program = """NOT B J"""
    #   #####...#########
    program = """NOT C J"""
    #   #####...#########
    program = """NOT D J"""
    #   #####.###########

    # BRUTE FORCING
    # solve()
    program = """NOT C J
NOT A T
OR T J
AND D J"""
    print(explore(computer, program)[0])

    # BRUTE FORCING find all possible part 1 programs
    # solve(program.split("\n"), stop=False, max_n=2)
    all_programs = """NOT C J
NOT A T
OR T J
AND D J

NOT C T
NOT A J
OR T J
AND D J

NOT A J
NOT C T
OR T J
AND D J

NOT A T
NOT C J
OR T J
AND D J

OR C T
AND A T
NOT T J
AND D J

OR A T
AND C T
NOT T J
AND D J

OR C J
AND A J
NOT J J
AND D J

OR A J
AND C J
NOT J J
AND D J

NOT C T
NOT A J
AND D T
OR T J

NOT A J
NOT C T
AND D T
OR T J

NOT C J
NOT A T
AND D J
OR T J

NOT A T
NOT C J
AND D J
OR T J

NOT C J
AND D J
NOT A T
OR T J

NOT C T
AND D T
NOT A J
OR T J

NOT D T
OR C T
AND A T
NOT T J

NOT D J
OR C J
AND A J
NOT J J"""

    # Part 1: seeing only 4 squares, jump if A or B or C are holed but not D
    #     so: J = (not A or not B or not C) and D
    #
    # Part 2: seeing 9 squares, part 1 + (E or H) (fifth or eighth square)
    #     so J = (not A or not B or not C) and D and (E or H)
    program = """NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
NOT D T
NOT T T
AND T J
NOT E T
NOT T T
OR H T
AND T J"""
    print(explore(computer, program, end="RUN")[0])
