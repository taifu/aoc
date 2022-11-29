class Instruction:
    pass
    def __init__(self, condition):
        self.condition = condition

class Program:
    def __init__(self, start):
        self.start = start

    def run(self):
        step = 0
        state = self.start
        tape = [0] * 100000
        pos = len(tape) // 2
        while step < self.steps:
            bit = tape[pos]
            what = self.instructions[state].states[bit]
            tape[pos] = what[0]
            pos += what[1]
            if pos < 0:
                pos = 0
                tape.insert(0, 0)
            elif pos == len(tape):
                tape.append(0, 0)
            state = what[2]
            step += 1
        return sum(tape)


def load(filename):
    instructions = {}
    for n, line in enumerate(open(filename).readlines()):
        line = line.strip()
        if n == 0:
            program = Program(line[-2])
        elif n == 1:
            program.steps = int(line.split()[-2])
        else:
            n -= 2
            if n % 10 == 0:
                bulk = []
            elif n % 10 == 1:
                instruction = Instruction(line[-2])
            elif 1 <  n % 10:
                bulk.append(line)
                if n % 10 == 9:
                    instruction.states = {}
                    for state in (0, 1):
                        pos = 1 + 4 * state
                        instruction.states[state] = (int(bulk[pos][-2]),  # write
                                                     -1 if bulk[pos + 1 ][-5:-1] == "left" else 1,  # move
                                                     bulk[pos + 2][-2])   # next_state
                    instructions[instruction.condition] = instruction
    program.instructions = instructions 
    return program

program = load("input")
print(program.run())
