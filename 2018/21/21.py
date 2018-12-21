REGISTER = 6


class CPU:
    def __init__(self, raw):
        self.load(raw)

    def reset(self, reg0):
        values = [0] * REGISTER
        values[0] = reg0
        self.registers = list(values)

    def compile(self, data):
        parts = data.split()
        return [getattr(self, "op_" + parts[0])] + [int(p) for p in parts[1:]]

    def load(self, raw):
        self.program = []
        lines = [line.strip() for line in raw.split("\n") if line.strip()]
        while lines:
            line = lines.pop(0)
            if line[0] == "#":
                self.r_ip = int(line.split()[-1])
            else:
                self.program.append(self.compile(line))

    def op_addr(self, ops):
        self.registers[ops[2]] = self.registers[ops[0]] + self.registers[ops[1]]

    def op_addi(self, ops):
        self.registers[ops[2]] = self.registers[ops[0]] + ops[1]

    def op_mulr(self, ops):
        self.registers[ops[2]] = self.registers[ops[0]] * self.registers[ops[1]]

    def op_muli(self, ops):
        self.registers[ops[2]] = self.registers[ops[0]] * ops[1]

    def op_banr(self, ops):
        self.registers[ops[2]] = self.registers[ops[0]] & self.registers[ops[1]]

    def op_bani(self, ops):
        self.registers[ops[2]] = self.registers[ops[0]] & ops[1]

    def op_borr(self, ops):
        self.registers[ops[2]] = self.registers[ops[0]] | self.registers[ops[1]]

    def op_bori(self, ops):
        self.registers[ops[2]] = self.registers[ops[0]] | ops[1]

    def op_setr(self, ops):
        self.registers[ops[2]] = self.registers[ops[0]]

    def op_seti(self, ops):
        self.registers[ops[2]] = ops[0]

    def op_gtir(self, ops):
        self.registers[ops[2]] = 1 if ops[0] > self.registers[ops[1]] else 0

    def op_gtri(self, ops):
        self.registers[ops[2]] = 1 if self.registers[ops[0]] > ops[1] else 0

    def op_gtrr(self, ops):
        self.registers[ops[2]] = 1 if self.registers[ops[0]] > self.registers[ops[1]] else 0

    def op_eqir(self, ops):
        self.registers[ops[2]] = 1 if ops[0] == self.registers[ops[1]] else 0

    def op_eqri(self, ops):
        self.registers[ops[2]] = 1 if self.registers[ops[0]] == ops[1] else 0

    def op_eqrr(self, ops):
        self.registers[ops[2]] = 1 if self.registers[ops[0]] == self.registers[ops[1]] else 0

    def run(self, reg0=0, steps=0):
        self.reset(reg0)
        step = ip = 0
        # Unica istruzione che usa il registro zero:
        # 29: eqrr 3 0 5
        threes = []
        while 0 <= ip < len(self.program):
            self.registers[self.r_ip] = ip
            line = self.program[ip]
            line[0](line[1:])
            # Unica istruzione che usa il registro zero:
            # 29: eqrr 3 0 5
            if ip == 29:
                three = self.registers[3]
                if three not in threes:
                    threes.append(three)
                    if steps > 0:
                        print(threes.pop())
                        return
                else:
                    print(threes[-1])
                    return
            ip = self.registers[self.r_ip]
            ip += 1
            step += 1
            if steps and step >= steps:
                break
        print("\nstopped")
        return self.registers[0]


cpu = CPU(open("input.txt").read())

cpu.run(steps=100000)
print("ended")
cpu.run()
