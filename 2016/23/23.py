def get_val(registers, reg):
    try:
        return registers[reg]
    except:
        return int(reg)


def execute(program, registers):
    CPY, INC, DEC, JNZ, TGL = 'cpy', 'inc', 'dec', 'jnz', 'tgl'

    step = 0

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
        step += 1

    return registers


program = [l.strip().split(" ") for l in open("input").readlines()]
print(execute(program, {'a': 7, 'b': 0, 'c': 0, 'd': 0})['a'])

# In realtà fa il fattoriale del registro 'a' e somma 94*99 che sono le
# costanti in due istruzioni sul fondo del programma

program = [l.strip().split(" ") for l in open("input").readlines()]
print(execute(program, {'a': 12, 'b': 0, 'c': 0, 'd': 0})['a'])

