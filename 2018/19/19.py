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

    def run(self, reg0=0, show=False):
        self.reset(reg0)
        ip = 0
        # print(self.r_ip)
        while 0 <= ip < len(self.program):
            self.registers[self.r_ip] = ip
            line = self.program[ip]
            if show:
                out = "{} {}".format(str(ip).rjust(2), str(self.registers).ljust(35))
                out += ("{} {}".format(str(line[0]).replace(".", " ").split()[2][3:8], line[1:]))
            line[0](line[1:])
            if show:
                print(out)
                print("   " + str(self.registers))
                print()
            ip = self.registers[self.r_ip]
            ip += 1
        return self.registers[0]


raw_example = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
"""

raw = open("input.txt").read()


cpu = CPU(raw_example)
print(cpu.run())

cpu = CPU(raw)
print(cpu.run())

# L'algoritmo somma tutti i fattori di un grande numero
# print(cpu.run(1, True))
# Si vede dopo pochi cicli che nizializza il secondo registro a 10551383
# Questi i suoi fattori primi:
#   43  59  4159

print(1 + 43 + 59 + 4159 + (43 * 59) + (43 * 4159) + (59 * 4159) + (43 * 59 * 4159))



