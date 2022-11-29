def load(filename):
    return [l.strip().split(" ") for l in open(filename).readlines()]


def get_val(registers, reg):
    if reg.isdigit() or reg[0] == '-':
        return int(reg)
    return registers[reg]


def execute(program, registers, debug=False):
    SET, SUB, MUL, JNZ = 'set', 'sub', 'mul', 'jnz'

    step = 0

    registers['m'] = 0

    while step < len(program):
        if debug:
            print(step, [[k, v] for k, v in sorted(registers.items()) if k != 'z'])
        instr, regs = program[step][0], program[step][1:]
        if instr == SET:
            registers[regs[0]] = get_val(registers, regs[1])
        elif instr in SUB:
            registers[regs[0]] = get_val(registers, regs[0]) - get_val(registers, regs[1])
        elif instr in MUL:
            registers[regs[0]] = get_val(registers, regs[0]) * get_val(registers, regs[1])
            registers['m'] += 1
        elif instr == JNZ:
            if get_val(registers, regs[0]) != 0:
                step += get_val(registers, regs[1]) - 1
        else:
            raise Exception("Instruction {} unmanaged".format(instr))
        step += 1

    return registers


registers = execute(load("input"), dict((chr(ord('a') + n), 0) for n in range(8)))
print(registers['m'])

# Second part

# Starting from the end and going back
#              COUNT FOR EVERY COMPOSITE FROM start to end
#   1 set b 84
#   2 set c b
#   3 jnz a 2
#   4 jnz 1 5
#   5 mul b 100
#   6 sub b -100000
#   7 set c b
#   8 sub c -17000
#   9 set f 1      <-----------------------------------------------------+
#  10 set d 2       d = 2                                                |
#  11 set e 2       e = 2                                                |
#  12 set g d       g = d                                                |
#  13 mul g e   F:  g = g*e  => g = d*e                                  |
#  14 sub g b   E:  g == 0 iff g == b => d*e == b                        |
#  15 jnz g 2                                                            |
#  16 set f 0   D:  set f=0 iff g == 0 => iff b = d*e => b is composite  |
#  17 sub e -1  G1: e increment 1 \                                      |
#  18 set g e                      \                                     |
#  19 sub g b                       \ till b - 1                         |
#  20 jnz g -8                                                           |
#  21 sub d -1  G2: d increment 1 \                                      |
#  22 set g d                      \                                     |
#  23 sub g b                       \ till b - 1                         |
#  24 jnz g -13                                                          |
#  25 jnz f 2                                                            |
#  26 sub h -1  C:  increment h iff f == 0                               |
#  27 set g b      g = b then \                                          |
#  28 sub g c                  \ sub c from g -> g == 0 iff b = c        |
#  29 jnz g 2   B: if g == 0 then 30 \                                   |
#  30 jnz 1                           \ exit                             |
#  31 sub b -17 A: add 17 to b (no other increments to b)                |
#  32 jnz 1 -23    ------------------------------------------------------+

program = load("input")
start = int(program[0][2]) * int(program[4][2]) - int(program[5][2])
end = start - int(program[7][2])
step = - int(program[30][2])

h = 0
for n in range(start, end + 1, step):
    for d in range(2, n):
        if n % d == 0:
            h += 1
            break
print(h)
