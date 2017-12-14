def get_val(registers, reg):
    try:
        return registers[reg]
    except:
        return int(reg)


def execute(program, registers):
    CPY, INC, DEC, JNZ = 'cpy', 'inc', 'dec', 'jnz'

    step = 0

    while step < len(program):
        instr, regs = program[step][0], program[step][1:]
        if instr == CPY:
            registers[regs[1]] = get_val(registers, regs[0])
        elif instr in (INC, DEC):
            registers[regs[0]] += 1 if instr == INC else -1
        elif instr == JNZ:
            if get_val(registers, regs[0]) != 0:
                step += int(regs[1]) - 1
        step += 1

    return registers


program = [l.strip().split(" ") for l in open("input").readlines()]

print(execute(program, {'a': 0, 'b': 0, 'c': 0, 'd': 0})['a'])
print(execute(program, {'a': 0, 'b': 0, 'c': 1, 'd': 0})['a'])
