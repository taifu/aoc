def get_val(registers, reg):
    try:
        return registers[reg]
    except:
        return int(reg)


def execute(program, registers, length=10):
    CPY, INC, DEC, JNZ, TGL, OUT = 'cpy', 'inc', 'dec', 'jnz', 'tgl', 'out'

    step = 0
    outputs = []

    while step < len(program):
        instr, regs = program[step][0], program[step][1:]
        if instr == CPY:
            registers[regs[1]] = get_val(registers, regs[0])
        elif instr in (INC, DEC):
            registers[regs[0]] += 1 if instr == INC else -1
        elif instr == JNZ:
            if get_val(registers, regs[0]) != 0:
                step += get_val(registers, regs[1]) - 1
        elif instr == TGL:
            pos = step + get_val(registers, regs[0])
            if pos < len(program):
                instr, regs = program[pos][0], program[step][1:]
                if instr in INC:
                    program[pos][0] = DEC
                elif instr in DEC:
                    program[pos][0] = INC
                elif instr == CPY:
                    program[pos][0] = JNZ
                elif instr == JNZ:
                    program[pos][0] = CPY
                elif instr == TGL:
                    program[pos][0] = INC
        elif instr == OUT:
            outputs.append(get_val(registers, regs[0]))
            if len(outputs) == length:
                return outputs

        step += 1


program = [l.strip().split(" ") for l in open("input").readlines()]

a, found = -1, False
while not found:
    a += 1
    length = 1
    while True:
        outputs = execute(program, {'a': a, 'b': 0, 'c': 0, 'd': 0}, length=length * 2)
        if outputs != [0, 1] * length:
            break
        if length > 20:
            found = True
            break
        length += 1

print(a, length)
