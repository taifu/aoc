class Sample:
    def __init__(self, before, istruction, after):
        self.before = before
        self.istruction = istruction
        self.after = after


class CPU:
    def __init__(self, raw):
        self.load(raw)

    def reset(self, values=None):
        if values is None:
            values = [0] * 4
        self.registers = list(values)

    def compile(self, data):
        if ":" in data:
            data = data.split("[")[1].replace(",", "")[:-1]
        return list(int(p) for p in data.split())

    def load(self, raw):
        self.samples = []
        self.program = []
        lines = [line.strip() for line in raw.split("\n") if line.strip()]
        while lines:
            line = lines.pop(0)
            if line[0] == "B":
                self.samples.append(Sample(self.compile(line), self.compile(lines.pop(0)), self.compile(lines.pop(0))))
            else:
                self.program.append(self.compile(line))

    def op0(self, ops):  # addr
        self.registers[ops[2]] = self.registers[ops[0]] + self.registers[ops[1]]

    def op1(self, ops):  # addi
        self.registers[ops[2]] = self.registers[ops[0]] + ops[1]

    def op2(self, ops):  # mulr
        self.registers[ops[2]] = self.registers[ops[0]] * self.registers[ops[1]]

    def op3(self, ops):  # muli
        self.registers[ops[2]] = self.registers[ops[0]] * ops[1]

    def op4(self, ops):  # banr
        self.registers[ops[2]] = self.registers[ops[0]] & self.registers[ops[1]]

    def op5(self, ops):  # bani
        self.registers[ops[2]] = self.registers[ops[0]] & ops[1]

    def op6(self, ops):  # borr
        self.registers[ops[2]] = self.registers[ops[0]] | self.registers[ops[1]]

    def op7(self, ops):  # bori
        self.registers[ops[2]] = self.registers[ops[0]] | ops[1]

    def op8(self, ops):  # setr
        self.registers[ops[2]] = self.registers[ops[0]]

    def op9(self, ops):  # seti
        self.registers[ops[2]] = ops[0]

    def op10(self, ops):  # gtir
        self.registers[ops[2]] = 1 if ops[0] > self.registers[ops[1]] else 0

    def op11(self, ops):  # gtri
        self.registers[ops[2]] = 1 if self.registers[ops[0]] > ops[1] else 0

    def op12(self, ops):  # gtrr
        self.registers[ops[2]] = 1 if self.registers[ops[0]] > self.registers[ops[1]] else 0

    def op13(self, ops):  # eqir
        self.registers[ops[2]] = 1 if ops[0] == self.registers[ops[1]] else 0

    def op14(self, ops):  # eqri
        self.registers[ops[2]] = 1 if self.registers[ops[0]] == ops[1] else 0

    def op15(self, ops):  # eqrr
        self.registers[ops[2]] = 1 if self.registers[ops[0]] == self.registers[ops[1]] else 0

    def guess(self):
        more_three = 0
        guesses = dict((op, set(range(16))) for op in range(16))
        for sample in self.samples:
            op_guess, istruction = sample.istruction[0], sample.istruction[1:]
            which = []
            for op in range(16):
                self.reset(sample.before)
                getattr(self, "op" + str(op))(istruction)
                if self.registers == sample.after:
                    which.append(op)
                    guesses[op_guess].add(op)
            if len(which) > 2:
                more_three += 1
            guesses[op_guess] = guesses[op_guess].intersection(set(which))
        while set(len(v) for v in guesses.values()) != set([1]):
            for op, values in guesses.items():
                values = list(values)
                if len(values) == 1:
                    value = values[0]
                    for k, v in guesses.items():
                        if k != op and value in v:
                            v.remove(value)
                            guesses[k] = v
        self.interpret = dict((k, getattr(self, "op" + str(list(v)[0]))) for k, v in guesses.items())
        return more_three

    def run(self):
        self.reset()
        for line in self.program:
            self.interpret[line[0]](line[1:])
        return self.registers[0]


cpu = CPU(open("input.txt").read())
print(cpu.guess())
print(cpu.run())
