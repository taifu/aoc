class CPU:
    def __init__(self, raw):
        self.load(raw)
        self.reset()

    def reset(self):
        self.accumulator = 0
        self.ip = 0

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

    def op_nop(self, ops):
        pass

    def op_acc(self, ops):
        self.accumulator += ops[0]

    def op_jmp(self, ops):
        self.ip += ops[0] - 1

    def run(self):
        self.reset()
        seen = set()
        while True:
            if self.ip in seen:
                return self.accumulator, False
            seen.add(self.ip)
            if self.ip == len(self.program):
                return self.accumulator, True
            elif self.ip > len(self.program):
                return self.accumulator, False
            line = self.program[self.ip]
            line[0](line[1:])
            self.ip += 1
        print("\nstopped")


def solve(data):
    cpu = CPU(data)
    return cpu.run()


def solve2(data):
    length = 0
    while True:
        cpu = CPU(data)
        op = cpu.program[length][0]
        if op == cpu.op_jmp:
            cpu.program[length][0] = cpu.op_nop
        elif op == cpu.op_nop:
            cpu.program[length][0] = cpu.op_jmp
        res, ok = cpu.run()
        if ok:
            return res
        length += 1


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve2(data))
